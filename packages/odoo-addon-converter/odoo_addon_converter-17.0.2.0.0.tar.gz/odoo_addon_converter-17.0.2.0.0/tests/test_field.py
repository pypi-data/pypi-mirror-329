##############################################################################
#
#    Converter Odoo module
#    Copyright © 2021 XCG Consulting <https://xcg-consulting.fr>
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

from odoo import tests  # type: ignore[import-untyped]

from .. import Field, TranslatedSelection


class Test(tests.TransactionCase):
    def setUp(self):
        super().setUp()
        self.active_user = self.env["res.users"].search(
            [("active", "=", True)], limit=1
        )
        self.inactive_user = self.env["res.users"].search(
            [("active", "=", False)], limit=1
        )

    def test_boolean_field(self):
        converter = Field("active")
        self.assertEqual(True, converter.odoo_to_message(self.active_user))
        self.assertEqual(False, converter.odoo_to_message(self.inactive_user))

        values = converter.message_to_odoo(
            self.env, "update", True, self.active_user, True
        )
        self.active_user.write(values)
        self.assertTrue(self.active_user.active)
        values = converter.message_to_odoo(
            self.env, "update", False, self.active_user, True
        )
        self.active_user.write(values)
        self.assertFalse(self.active_user.active)
        values = converter.message_to_odoo(
            self.env, "update", False, self.inactive_user, True
        )
        self.inactive_user.write(values)
        self.assertFalse(self.inactive_user.active)
        values = converter.message_to_odoo(
            self.env, "update", True, self.inactive_user, True
        )
        self.inactive_user.write(values)
        self.assertTrue(self.inactive_user.active)

    def test_message_formatter(self):
        # convert active boolean to those values
        active = "Active"
        inactive = "Inactive"

        # define some formatter
        def message_formatter(value: Any, is_blank: bool) -> Any:
            return active if value else inactive

        def odoo_formatter(value: Any):
            return value == active

        converter = Field(
            "active",
            message_formatter=message_formatter,
            odoo_formatter=odoo_formatter,
        )
        self.assertEqual(active, converter.odoo_to_message(self.active_user))
        self.assertEqual(inactive, converter.odoo_to_message(self.inactive_user))

        # already active, should be an empty dict
        self.assertEqual(
            {},
            converter.message_to_odoo(
                self.env, "update", active, self.active_user, True
            ),
        )
        values = converter.message_to_odoo(
            self.env, "update", inactive, self.active_user, True
        )
        self.active_user.write(values)
        self.assertFalse(self.active_user.active)

    def test_translated_selection(self):
        converter = TranslatedSelection("target", "en_US")
        self.assertEqual(
            "New Window",
            converter.odoo_to_message(
                self.env["ir.actions.act_url"].search([("target", "=", "new")], limit=1)
            ),
        )
        self.assertEqual(
            "This Window",
            converter.odoo_to_message(
                self.env["ir.actions.act_url"].search(
                    [("target", "=", "self")], limit=1
                )
            ),
        )
