# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class IotDeviceInput(models.Model):
    _inherit = "iot.device.input"

    template_input_id = fields.Many2one(
        "iot.template.input",
        readonly=True,
    )

    def get_configuration(self):
        return {
            "serial": self.serial,
            "passphrase": self.passphrase,
        }
