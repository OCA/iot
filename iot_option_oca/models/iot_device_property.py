# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class IotDeviceProperty(models.Model):

    _name = "iot.device.property"
    _description = "Device Property"

    name = fields.Char(required=True, translate=True)
    tech_name = fields.Char(required=True)
    field_type = fields.Selection(
        selection=[
            ("str", "Text"),
            ("int", "Whole number"),
            ("float", "Decimal number"),
            ("bool", "Yes/No"),
            ("date", "Date"),
        ],
        compute="_compute_field_type",
        store=True,
    )
    widget = fields.Selection(
        selection=[
            ("boolean", "Boolean"),
            ("float", "Decimal"),
            ("integer", "Integer"),
            ("date", "Date"),
            ("char", "Single line text"),
            ("text", "Multi line Text"),
            ("html", "Complex text"),
        ],
        default="char",
        required=True,
        help="Type of information that can be stored in the property.",
    )
    default_value = fields.Char(
        translate=True,
        help="Will be applied by default to all custom values of this "
        "property. This is a char field, so you have to enter some value "
        "that can be converted to the field type you choose.",
    )
    required = fields.Boolean()
    is_action = fields.Boolean()

    @api.model
    def _get_field_type_map(self):
        return {
            "boolean": "bool",
            "float": "float",
            "integer": "int",
            "date": "date",
            "char": "str",
            "text": "str",
            "html": "str",
            "many2one": "id",
        }

    @api.depends("widget")
    def _compute_field_type(self):
        field_type_map = self._get_field_type_map()
        for record in self:
            record.field_type = field_type_map.get(record.widget, "str")
