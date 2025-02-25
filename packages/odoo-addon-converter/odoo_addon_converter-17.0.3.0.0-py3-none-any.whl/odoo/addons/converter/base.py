##############################################################################
#
#    Converter Odoo module
#    Copyright © 2020, 2025 XCG Consulting <https://xcg-consulting.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""Converter is a utility class that makes conversion very easy between
Odoo records & JSON dicts. It's very fast and extendable and convert both ways.

Supports aggregates of the form (simplified example JSON-schemas)::
    {"type": "object", "properties": { "items": { "type": "array", "items": {
        "type": "object", "properties": {
            "data": {"oneOf": [{"$ref": "user.json"}, {"$ref": "s2.json"}]}
        }
    }}}}
    ---
    {"$id": "user.json", "type": "object", "properties": {
        "__type__": {"type": "string", "enum": ["user"]},
        "name": {"type": "string"}
    }}
"""

import inspect
import logging
from abc import ABCMeta, abstractmethod
from collections.abc import Callable, Mapping
from typing import Any

from odoo import api, models  # type: ignore[import-untyped]

from .exception import InternalError
from .validate import Validation, Validator

logger = logging.getLogger(__name__)


class SkipType:
    def get__type__(self) -> set[str]:
        # Avoid conditions isinstance(converter, SkipType)
        return set()

    @property
    def possible_datatypes(self) -> set[str]:
        # Avoid conditions isinstance(converter, SkipType)
        return set()

    def odoo_datatype(self, instance: models.BaseModel) -> str | None:
        # Avoid conditions isinstance(converter, SkipType)
        return None


Skip = SkipType()


class NewinstanceType:
    pass


Newinstance = NewinstanceType()

Context = Mapping | None
ContextBuilder = Callable[[models.BaseModel, Context], Context]

PHASE_PRECREATE = "precreate"
PHASE_POSTCREATE = "postcreate"
PHASE_UPDATE = "UPDATE"

OPERATION_CREATION = "create"
OPERATION_UPDATE = "update"


def build_context(
    instance: models.BaseModel | None,
    ctx: Context,
    extend: ContextBuilder | None,
) -> Context:
    if instance is None:
        return ctx
    if extend:
        if ctx is None:
            ctx = {}
        else:
            ctx = dict(ctx)
        extended = extend(instance, None)
        if extended is not None:
            ctx.update(extended)
    return ctx


class NotAnInstanceGetterException(Exception):
    def __init__(self):
        super().__init__("Not an instance getter")


class Converter:
    """Base converter class.
    It does not actually convert anything.
    """

    def __init__(self):
        self._validation: Validation = Validation.SKIP

    def odoo_to_message(self, instance: models.BaseModel, ctx: Context = None) -> Any:
        """From an instance, this method returns a matching value for the
        message field.
        :param instance: an instance of an Odoo model
        :param ctx: context value
        :return: The value or Skip if not included in the message.
        """
        return Skip

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        phase: str,
        message_value: Any,
        instance: models.BaseModel,
        value_present: bool = True,
    ) -> dict | SkipType:
        """From a message, returns a dict.
        Only field whose values are changed are included in the returned dict.
        :param odoo_env: odoo environment
        :param phase: precreate, postcreate, update
        :param message_value: the value of the message
        :param instance: an odoo instance, used to remove existing value from
        the produced dict as needed
        :param value_present: indicate if the value was actually in the message
        (in order to differentiate given None values to non provided values)
        :return: dict of changes to apply on an instance (if any).
        """
        return {}

    @property
    def is_instance_getter(self) -> bool:
        return False

    # XXX should that be moved to a different class, like PostHookConverter
    def get_instance(
        self, odoo_env: api.Environment, message_data
    ) -> models.BaseModel | NewinstanceType | None:
        """Return an instance of a model. Check is_instance_getter before calling"""
        raise NotAnInstanceGetterException()

    def get__type__(self) -> set[str]:
        """Indicate if this converter is associated to several __type__.
        If so, it will be called with incoming messages associated to them.
        (using message_to_odoo)"""
        return set()

    @property
    def validator(self) -> Validator | None:
        """A validator to use for validation of created messages"""
        return self._get_validator()

    @validator.setter
    def validator(self, value: Validator | None) -> None:
        self._set_validator(value)

    def _get_validator(self) -> Validator | None:
        return self._validator

    def _set_validator(self, value: Validator | None) -> None:
        if value is None:
            self._validator = None
        else:
            if value.initialized:
                self._validator = value
            else:
                raise InternalError(
                    "you must initialize() the validator before passing it"
                )

    @property
    def validation(self) -> Validation:
        return self._get_validation()

    @validation.setter
    def validation(self, value: Validation) -> None:
        self._set_validation(value)

    def _get_validation(self) -> Validation:
        return self._validation

    def _set_validation(self, value: Validation) -> None:
        """Define if validation should be done"""
        assert value is not None
        self._validation = value

    @property
    def possible_datatypes(self) -> set[str]:
        """Possible values for datatype."""
        # A set, as for get___type__, to allow switch to handle different messages.
        return set()

    def odoo_datatype(self, instance: models.BaseModel) -> str | None:
        return None


class PostHookConverter(Converter, metaclass=ABCMeta):
    @abstractmethod
    def post_hook(self, instance: models.BaseModel, message_data):
        """Post hook"""


class Readonly(Converter):
    def __init__(self, conv: Converter):
        super().__init__()
        self._conv = conv

    def odoo_to_message(self, instance: models.BaseModel, ctx: Context = None) -> Any:
        return self._conv.odoo_to_message(instance, ctx)

    def odoo_datatype(self, instance: models.BaseModel) -> str | None:
        return self._conv.odoo_datatype(instance)


class Writeonly(Converter):
    """A converter that only convert to odoo but does nothing from odoo."""

    def __init__(self, conv: Converter):
        super().__init__()
        self._conv = conv

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        phase: str,
        message_value: Any,
        instance: models.BaseModel,
        value_present: bool = True,
    ) -> dict | SkipType:
        return self._conv.message_to_odoo(
            odoo_env, phase, message_value, instance, value_present
        )

    @property
    def is_instance_getter(self) -> bool:
        return self._conv.is_instance_getter

    def get_instance(
        self, odoo_env: api.Environment, message_data
    ) -> models.BaseModel | NewinstanceType | None:
        return self._conv.get_instance(odoo_env, message_data)

    @property
    def possible_datatypes(self) -> set[str]:
        return self._conv.possible_datatypes


class Computed(Converter):
    def __init__(self, from_odoo: Callable[[models.BaseModel, Context], Any]):
        self.from_odoo = from_odoo

        sig = inspect.signature(from_odoo)
        self.from_odoo_arg_count = len(sig.parameters)
        if self.from_odoo_arg_count not in (1, 2):
            raise ValueError(
                "Computed 'from_odoo' callback must have 1 or 2 args: got "
                f"{self.from_odoo_arg_count}"
            )

    def odoo_to_message(self, instance: models.BaseModel, ctx: Context = None) -> Any:
        if self.from_odoo_arg_count == 1:
            return self.from_odoo(instance, None)
        return self.from_odoo(instance, ctx)


class Constant(Converter):
    """When building messages, this converter return a constant value."""

    def __init__(self, value: Any):
        self._value = value

    def odoo_to_message(self, instance: models.BaseModel, ctx: Context = None) -> Any:
        return self._value


def message_to_odoo(
    odoo_env: api.Environment,
    payload: Mapping,
    model_name: str,
    converter: Converter,
    operation: str | None = None,
) -> models.BaseModel:
    """

    :param odoo_env: an Odoo environment
    :param payload: received data
    :param model_name: name of an Odoo model
    :param converter:
    :param operation: if operation is not given, creation will be done if no
       instance can be found by using
       :py:meth:odoo.addons.Converter.get_instance
    :return:
    """
    instance: NewinstanceType | models.BaseModel
    if operation == OPERATION_CREATION:
        instance = Newinstance
    else:
        instance = converter.get_instance(odoo_env, payload)
    if operation == OPERATION_CREATION or (
        operation is None and not instance or instance is Newinstance
    ):
        changes = converter.message_to_odoo(
            odoo_env, PHASE_PRECREATE, payload, instance
        )
        if isinstance(changes, SkipType):
            return odoo_env[model_name]

        instance = odoo_env[model_name].create(changes)
        changes = converter.message_to_odoo(
            odoo_env, PHASE_POSTCREATE, payload, instance
        )
        if changes:
            instance.write(changes)
    if operation == OPERATION_UPDATE or not (
        operation is None and not instance or instance is Newinstance
    ):
        changes = converter.message_to_odoo(odoo_env, PHASE_UPDATE, payload, instance)
        if isinstance(changes, SkipType):
            return odoo_env[model_name]

        if changes:
            instance.write(changes)
    if hasattr(converter, "post_hook"):
        converter.post_hook(instance, payload)
    return instance
