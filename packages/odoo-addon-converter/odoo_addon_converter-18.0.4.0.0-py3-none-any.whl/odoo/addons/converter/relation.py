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
from collections.abc import Callable
from typing import Any

from odoo import api, models  # type: ignore[import-untyped]

from .base import (
    Context,
    ContextBuilder,
    Converter,
    NewinstanceType,
    Skip,
    SkipType,
    build_context,
)
from .field import Field

_logger = logging.getLogger(__name__)


class RelationToOne(Field):
    def __init__(
        self,
        field_name: str,
        model_name: str | None,
        converter: Converter,
        send_empty: bool = True,
        context: ContextBuilder | None = None,
    ):
        super().__init__(field_name)
        self.converter = converter
        self.model_name = model_name
        self._send_empty = send_empty
        self.context = context

    def odoo_to_message(self, instance: models.BaseModel, ctx: Context = None) -> Any:
        ctx = build_context(instance, ctx, self.context)
        # do not use super, otherwise if empty, will convert that
        relation_instance = getattr(instance, self.field_name)
        if not relation_instance:
            if not self._send_empty:
                return Skip
            else:
                relation_instance = instance.env[self.model_name]
        return self.converter.odoo_to_message(relation_instance, ctx)

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        phase: str,
        message_value: Any,
        instance: models.BaseModel,
        value_present: bool = True,
    ) -> dict | SkipType:
        if not value_present:
            return {}

        record = _update_record(
            self, odoo_env, phase, message_value, instance, value_present
        )
        if record is None:
            return {}

        return {self.field_name: record.id}


class RelationToMany(Field):
    def __init__(
        self,
        field_name: str,
        model_name: str | None,
        converter: Converter,
        sortkey: None | Callable[[models.BaseModel], bool] = None,
        filtered: None | str | Callable[[models.BaseModel], bool] = None,
        context: ContextBuilder | None = None,
        limit: Any | None = None,
    ):
        """
        :param filtered: filter to use in Odoo’s BaseModel filtered method.
        """
        super().__init__(field_name)
        self.converter = converter
        self.model_name = model_name
        self.filtered = filtered
        self.sortkey = sortkey
        self.context = context
        self.limit = limit

    def odoo_to_message(self, instance: models.BaseModel, ctx: Context = None) -> Any:
        ctx = build_context(instance, ctx, self.context)
        value = super().odoo_to_message(instance, ctx)
        if isinstance(value, SkipType):
            return value
        if self.filtered:
            value = value.filtered(self.filtered)
        if self.sortkey:
            value = value.sorted(key=self.sortkey)
        if self.limit:
            value = value[: self.limit]

        return [
            m
            for m in (self.converter.odoo_to_message(r, ctx) for r in value)
            if not isinstance(m, SkipType)
        ]

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        phase: str,
        message_value: Any,
        instance: models.BaseModel,
        value_present: bool = True,
    ) -> dict | SkipType:
        # if not present or value is None, do not update the values.
        if not value_present or message_value is None:
            return {}
        field_instances = odoo_env[self.model_name]
        for value in message_value:
            record = _update_record(
                self, odoo_env, phase, value, instance, value_present
            )
            if record is not None:
                field_instances |= record

        if (
            instance
            and not isinstance(instance, NewinstanceType)
            and getattr(instance, self.field_name) == field_instances
        ):
            return {}
        return {self.field_name: [(6, 0, field_instances.ids)]}


class RelationToManyMap(Field):
    def __init__(
        self,
        field_name: str,
        model_name: str | None,
        key_converter: Converter,
        value_converter: Converter,
        filtered: None | str | Callable[[models.BaseModel], bool] = None,
        context: ContextBuilder | None = None,
    ):
        """
        :param filtered: filter to use in Odoo’s BaseModel filtered method.
        """
        super().__init__(field_name)
        self.key_converter = key_converter
        self.value_converter = value_converter
        self.model_name = model_name
        self.filtered = filtered
        self.context = context

    def odoo_to_message(self, instance: models.BaseModel, ctx: Context = None) -> Any:
        ctx = build_context(instance, ctx, self.context)
        value = super().odoo_to_message(instance, ctx)
        if isinstance(value, SkipType):
            return value
        if self.filtered:
            value = value.filtered(self.filtered)
        return {
            k: v
            for k, v in (
                (
                    self.key_converter.odoo_to_message(r, ctx),
                    self.value_converter.odoo_to_message(r, ctx),
                )
                for r in value
            )
            if not isinstance(k, SkipType) and not isinstance(v, SkipType)
        }

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        phase: str,
        message_value: Any,
        instance: models.BaseModel,
        value_present: bool = True,
    ) -> dict | SkipType:
        # if not present or value is None, do not update the values.
        if not value_present or message_value is None:
            return {}
        field_instances = odoo_env[self.model_name]
        for value in message_value:
            record = _update_record(
                self, odoo_env, phase, value, instance, value_present
            )
            if record is not None:
                field_instances |= record

        if (
            instance
            and not isinstance(instance, NewinstanceType)
            and getattr(instance, self.field_name) == field_instances
        ):
            return {}
        return {self.field_name: [(6, 0, field_instances.ids)]}


def relation(path: str, converter: Converter) -> Converter:
    for name in reversed(path.split("/")):
        model_name = None
        pi = name.find("(")
        if pi != -1:
            if not name.endswith(")"):
                raise ValueError("Invalid path: %s", name)
            model_name = name[pi + 1 : -1]  # noqa: E203
            name = name[:pi]
        if name.endswith("[]"):
            converter = RelationToMany(name[:-2], model_name, converter)
        else:
            converter = RelationToOne(name, model_name, converter)
    return converter


def _update_record(
    self,
    odoo_env: api.Environment,
    phase: str,
    message_value: Any,
    instance: models.BaseModel,
    value_present: bool = True,
) -> Any:
    """Update or create a single record with the given values.
    :param self: the actual converter class.
    :param message_value: the message value for one record.
    :return: the record id, if any, else None.
    """
    post_hook = getattr(self.converter, "post_hook", None)

    if self.converter.is_instance_getter:
        rel_record: models.BaseModel | NewinstanceType | None = (
            self.converter.get_instance(odoo_env, message_value)
        )
        if rel_record is None:
            return None

        if isinstance(rel_record, NewinstanceType):
            rel_record = None

        updates = self.converter.message_to_odoo(
            odoo_env, phase, message_value, rel_record, value_present
        )

        if updates:
            if rel_record:
                rel_record.write(updates)
            else:
                rel_record = odoo_env[self.model_name].create(updates)
            if post_hook:
                post_hook(rel_record, message_value)

        if instance and not isinstance(instance, NewinstanceType):
            field_value = getattr(instance, self.field_name)
            if field_value and rel_record.id in field_value.ids:
                return None

        return rel_record
    else:
        field_value = (
            getattr(instance, self.field_name)
            if instance and not isinstance(instance, NewinstanceType)
            else None
        )

        updates = self.converter.message_to_odoo(
            odoo_env, phase, message_value, field_value, value_present
        )

        if updates:
            if field_value:
                field_value.write(updates)
                if post_hook:
                    post_hook(field_value, message_value)
                return None
            else:
                rel_record = odoo_env[self.model_name].create(updates)
                if post_hook:
                    post_hook(rel_record, message_value)
                return rel_record
        return None
