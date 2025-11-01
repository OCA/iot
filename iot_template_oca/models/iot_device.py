# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class IotDevice(models.Model):
    _inherit = "iot.device"

    def get_iot_configuration(self):
        self.ensure_one()
        return {
            "host": self.env["ir.config_parameter"].sudo().get_param("web.base.url"),
            "name": self.name,
            "outputs": {
                output.name: output.get_configuration() for output in self.output_ids
            },
            "inputs": {
                iot_input.name: iot_input.get_configuration()
                for iot_input in self.input_ids
            },
        }
