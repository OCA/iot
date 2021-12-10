# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IotTemplate(models.Model):

    _inherit = "iot.template"

    property_ids = fields.Many2many("iot.device.property")

    def apply_template(self, device, keys):
        super(IotTemplate, self).apply_template(device, keys)
        for prop in self.property_ids:
            self.env["iot.device.option"].create(self._create_option_vals(device, prop))

    def _create_option_vals(self, device, prop):
        vals = {
            "device_id": device.id,
            "property_id": prop.id,
        }
        if prop.default_value:
            vals["value_%s" % prop.field_type] = prop.default_value
        return vals
