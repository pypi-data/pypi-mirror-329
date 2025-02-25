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

from . import models
from .base import (
    OPERATION_CREATION,
    OPERATION_UPDATE,
    PHASE_POSTCREATE,
    PHASE_PRECREATE,
    PHASE_UPDATE,
    Computed,
    Constant,
    Context,
    ContextBuilder,
    Converter,
    Newinstance,
    NewinstanceType,
    Readonly,
    Skip,
    SkipType,
    Writeonly,
    message_to_odoo,
    build_context,
)
from .exception import InternalError
from .field import Field, TranslatedSelection
from .keyfield import KeyField
from .list import List
from .mail_template import MailTemplate
from .model import Model
from .relation import RelationToMany, RelationToManyMap, RelationToOne, relation
from .switch import Switch
from .validate import (
    Validation,
    NotInitialized,
    Validator,
)
from .xref import Xref
