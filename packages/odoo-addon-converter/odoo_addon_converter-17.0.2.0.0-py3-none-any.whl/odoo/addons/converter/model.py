##############################################################################
#
#    Converter Odoo module
#    Copyright © 2020, 2024 XCG Consulting <https://xcg-consulting.fr>
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
import logging
import traceback
from collections import OrderedDict
from collections.abc import Iterable, Mapping
from typing import Any, Final

import fastjsonschema  # type: ignore[import-untyped]
from odoo import _, api, models  # type: ignore[import-untyped]
from odoo.exceptions import UserError  # type: ignore[import-untyped]

from .base import (
    Context,
    ContextBuilder,
    Converter,
    Newinstance,
    NewinstanceType,
    PostHookConverter,
    SkipType,
    build_context,
)
from .validate import NotInitialized, Validation, Validator

_logger = logging.getLogger(__name__)


class IncorrectTypeException(Exception):
    """__type__ is in the message is not the same as the expected value"""


class MissingRequiredValidatorException(Exception):
    def __init__(self):
        super().__init__("Strict validation without validator")


class Model(PostHookConverter):
    """A converter that takes a dict of key, used when a message has values"""

    def __init__(
        self,
        converters: Mapping[str, Converter],
        json_schema: str | None = None,
        # The validator is usually not given at this point but is common
        # throughout a project. That’s why it is a property
        validator: Validator | None = None,
        merge_with: Iterable[Converter] | None = None,
        validation: Validation = Validation.SKIP,
        context: ContextBuilder | None = None,
        datatype: str | None = None,
        __type__: str | None = None,
    ):
        """
        :param datatype: datatype to use. Usually used with None __type__.
        """
        super().__init__()
        self._type: str | None = __type__
        self._converters: Mapping[str, Converter] = converters
        self._post_hooks_converters: dict[str, PostHookConverter] = {}
        self._jsonschema: str | None = json_schema
        self._get_instance: str | None = None
        """First converter whose `is_instance_getter` is true if any"""
        self.merge_with: Iterable[Converter] | None = merge_with
        self.context: ContextBuilder | None = context
        self.validator = validator
        self.validation = validation
        self._datatype: Final[str | None] = datatype

        for key, converter in converters.items():
            if self._get_instance is None and converter.is_instance_getter:
                self._get_instance = key
            if isinstance(converter, PostHookConverter):
                self._post_hooks_converters[key] = converter

    def odoo_to_message(self, instance: models.BaseModel, ctx: Context = None) -> Any:
        ctx = build_context(instance, ctx, self.context)

        message_data = {}
        if self._type is not None:
            message_data["__type__"] = self._type

        errors = []
        for key in self._converters:
            try:
                value = self._converters[key].odoo_to_message(instance, ctx)
            except Exception as e:
                errors.append(
                    {"key": key, "traceback": "".join(traceback.format_exception(e))}
                )
                continue
            if not isinstance(value, SkipType):
                message_data[key] = value
        if len(errors) != 0:
            formatted_errors = "\n\n".join(
                [f"{error['traceback']}Key: {error['key']}" for error in errors]
            )
            raise UserError(
                _(
                    "Got unexpected errors while parsing substitutions:\n%s",
                    formatted_errors,
                )
            )

        if self.merge_with:
            for conv in self.merge_with:
                value = conv.odoo_to_message(instance, ctx)
                if isinstance(value, SkipType):
                    continue
                message_data.update(value)

        if self.validation != Validation.SKIP and self._jsonschema is not None:
            if self.validator:
                try:
                    self.validator.validate(self._jsonschema, message_data)
                except (NotInitialized, fastjsonschema.JsonSchemaException):
                    _logger.warning("Validation failed", exc_info=True)
                    if self.validation == Validation.STRICT:
                        raise
            elif self.validation == Validation.STRICT:
                raise MissingRequiredValidatorException()

        return message_data

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        phase: str,
        message_value: Any,
        instance: models.BaseModel,
        value_present: bool = True,
    ) -> dict | SkipType:
        values: dict[str, Any] = OrderedDict()

        if self.validation != Validation.SKIP and self._jsonschema is not None:
            if self.validator:
                try:
                    self.validator.validate(self._jsonschema, message_value)
                except (NotInitialized, fastjsonschema.JsonSchemaException):
                    _logger.warning("Validation failed", exc_info=True)
                    if self.validation == Validation.STRICT:
                        raise
            elif self.validation == Validation.STRICT:
                raise MissingRequiredValidatorException()

        if self._type is not None and message_value["__type__"] != self._type:
            raise IncorrectTypeException(
                "Expected __type__ {}, found {}".format(
                    self._type, message_value["__type__"]
                )
            )
        for key in self._converters:
            value = message_value.get(key, None) if message_value else None
            attribute_vals = self._converters[key].message_to_odoo(
                odoo_env,
                phase,
                value,
                instance,
                message_value and key in message_value,
            )
            if isinstance(attribute_vals, SkipType):
                continue
            values.update(attribute_vals)
        if self.merge_with:
            for conv in self.merge_with:
                value = conv.message_to_odoo(
                    odoo_env, phase, message_value, instance, value_present
                )
                if isinstance(value, SkipType):
                    continue
                values.update(value)

        return values

    @property
    def is_instance_getter(self) -> bool:
        return self._get_instance is not None

    def get_instance(
        self, odoo_env: api.Environment, message_data
    ) -> models.BaseModel | NewinstanceType | None:
        """:return: an instance linked to the converter, if any"""
        if self._get_instance:
            instance = self._converters[self._get_instance].get_instance(
                odoo_env, message_data[self._get_instance]
            )
            if instance is None:
                instance = Newinstance
            return instance
        return None

    def post_hook(self, instance: models.BaseModel, message_data):
        for key in self._post_hooks_converters:
            if key in message_data:
                self._post_hooks_converters[key].post_hook(instance, message_data[key])
        if self.merge_with:
            for converter in self.merge_with:
                if hasattr(converter, "post_hook"):
                    converter.post_hook(instance, message_data)

    def get__type__(self) -> set[str]:
        return set() if self._type is None else {self._type}

    @property
    def possible_datatypes(self) -> set[str]:
        result = set()
        if self._datatype is not None:
            result.add(self._datatype)
        return result

    def odoo_datatype(self, instance: models.BaseModel) -> str | None:
        return self._datatype
