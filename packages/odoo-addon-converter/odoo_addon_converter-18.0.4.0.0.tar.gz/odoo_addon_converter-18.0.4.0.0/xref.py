##############################################################################
#
#    Converter Odoo module
#    Copyright © 2020 XCG Consulting <https://xcg-consulting.fr>
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

from typing import Any

from odoo import api, models  # type: ignore[import-untyped]

from .base import Context, NewinstanceType, PostHookConverter
from .models.ir_model_data import _XREF_IMD_MODULE


# TODO dans quel cas ça ne pourrait pas être un instance getter???
class Xref(PostHookConverter):
    """This converter represents an external reference, using the standard xmlid with a
    custom module name.
    """

    def __init__(
        self, module: str | None = _XREF_IMD_MODULE, is_instance_getter: bool = True
    ):
        super().__init__()
        self._module = module
        self._is_instance_getter = is_instance_getter

    def odoo_to_message(self, instance: models.BaseModel, ctx: Context = None) -> Any:
        if not instance:
            return ""
        return instance.env["ir.model.data"].object_to_xmlid(
            instance, module=self._module
        )

    def get_instance(
        self, odoo_env: api.Environment, message_data
    ) -> models.BaseModel | NewinstanceType | None:
        if self._is_instance_getter:
            return odoo_env.ref(
                ".".join(["" if self._module is None else self._module, message_data]),
                raise_if_not_found=False,
            )
        return None

    def post_hook(self, instance: models.BaseModel, message_data):
        # add xmlid to the newly created object
        instance.env["ir.model.data"].set_xmlid(
            instance, message_data, module=self._module, only_when_missing=True
        )

    @property
    def is_instance_getter(self) -> bool:
        return self._is_instance_getter
