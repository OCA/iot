# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models


class IotDeviceOutput(models.Model):
    _inherit = 'iot.device.output'

    @api.multi
    def get_configuration(self):
        return {

        }
