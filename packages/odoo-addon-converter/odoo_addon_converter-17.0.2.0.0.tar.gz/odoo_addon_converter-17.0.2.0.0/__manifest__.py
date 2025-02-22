##############################################################################
#
#    Converter Odoo module
#    Copyright © 2020-2025 XCG Consulting <https://xcg-consulting.fr>
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
{
    "name": "Converter",
    "license": "AGPL-3",
    "summary": "Convert odoo records to/from plain data structures.",
    "version": "17.0.2.0.0",
    "category": "Hidden",
    "author": "XCG Consulting",
    "website": "https://orbeet.io/",
    "depends": ["base"],
    "installable": True,
    "external_dependencies": {"python": ["fastjsonschema"]},
}
