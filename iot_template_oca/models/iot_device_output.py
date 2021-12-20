# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class IotDeviceOutput(models.Model):
    _inherit = "iot.device.output"

    template_output_id = fields.Many2one(
        "iot.template.output",
        readonly=True,
    )

    def get_configuration(self):
        return {}
