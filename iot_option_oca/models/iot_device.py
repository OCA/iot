# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval


class IotDevice(models.Model):
    _inherit = "iot.device"

    option_ids = fields.One2many("iot.device.option", inverse_name="device_id",)


class IotDeviceOption(models.Model):
    _name = "iot.device.option"
    _description = "Device Option"

    _rec_name = "value"
    _order = "device_id, sequence, property_id"
    _sql_constraints = [
        (
            "property_device",
            "UNIQUE (property_id, device_id)",
            "Another property with that name exists for that device.",
        ),
    ]

    device_id = fields.Many2one("iot.device", required=True)
    property_id = fields.Many2one(
        comodel_name="iot.device.property", required=True, string="Property",
    )
    sequence = fields.Integer(index=True)
    name = fields.Char(related="property_id.name")
    field_type = fields.Selection(related="property_id.field_type")
    widget = fields.Selection(related="property_id.widget", readonly=True,)
    field_name = fields.Char(
        compute="_compute_field_name",
        help="Technical name of the field where the value is stored.",
    )
    required = fields.Boolean(related="property_id.required")
    value = fields.Char(
        compute="_compute_value",
        inverse="_inverse_value",
        search="_search_value",
        help="Value, always converted to/from the typed field.",
    )
    value_str = fields.Char(string="Text value", translate=True, index=True)
    value_int = fields.Integer(string="Whole number value", index=True)
    value_float = fields.Float(string="Decimal number value", index=True)
    value_bool = fields.Boolean(string="Yes/No value", index=True)
    value_date = fields.Date(string="Date value", index=True)

    @api.depends("property_id.field_type")
    def _compute_field_name(self):
        """Get the technical name where the real typed value is stored."""
        for s in self:
            s.field_name = "value_{!s}".format(s.property_id.field_type)

    @api.depends(
        "property_id.field_type",
        "field_name",
        "value_str",
        "value_int",
        "value_float",
        "value_bool",
    )
    def _compute_value(self):
        """Get the value as a string, from the original field."""
        for s in self:
            if s.field_type == "bool":
                s.value = _("Yes") if s.value_bool else _("No")
            else:
                s.value = getattr(s, s.field_name, False)

    def _inverse_value(self):
        """Write the value correctly converted in the typed field."""
        for record in self:
            record[record.field_name] = self._transform_value(
                record.value, record.field_type, record.property_id,
            )

    @api.constrains(
        "value_str",
        "value_int",
        "value_float",
        "value_bool",
        "value_date",
        "property_id",
    )
    def _check_required(self):
        for record in self:
            if not record.required:
                continue
            if not record.value:
                raise ValidationError(
                    _("Some required elements have not been fulfilled")
                )

    @api.onchange("property_id")
    def _onchange_property_set_default_value(self):
        """Load default value for this property."""
        for record in self:
            if not record.value and record.property_id.default_value:
                record.value = record.property_id.default_value
            if not record.field_type and record.property_id.field_type:
                record.field_type = record.property_id.field_type

    @api.onchange("value")
    def _onchange_value(self):
        """Inverse function is not launched after writing, so we need to
        trigger it right now."""
        self._inverse_value()

    @api.model
    def _transform_value(self, value, format_, properties=None):
        """Transforms a text value to the expected format.

        :param str/bool value:
            Custom value in raw string.

        :param str format_:
            Target conversion format for the value. Must be available among
            ``custom.info.property`` options.

        :param recordset properties:
            Useful when :param:`format_` is ``id``, as it helps to ensure the
            option is available in these properties. If :param:`format_` is
            ``id`` and :param:`properties` is ``None``, no transformation will
            be made for :param:`value`.
        """
        if not value:
            value = False
        elif format_ == "id" and properties:
            value = self.env["custom.info.option"].search(
                [
                    ("property_ids", "in", properties.ids),
                    ("name", "ilike", u"%{}%".format(value)),
                ],
                limit=1,
            )
        elif format_ == "bool":
            value = value.strip().lower() not in {
                "0",
                "false",
                "",
                "no",
                "off",
                _("No").lower(),
            }
        elif format_ in {"date"}:
            value = fields.Date.from_string(value)
        elif format_ in {"datetime"}:
            value = fields.Datetime.from_string(value)
        elif format_ not in {"str", "id"}:
            value = safe_eval("{!s}({!r})".format(format_, value))
        return value
