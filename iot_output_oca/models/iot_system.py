# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class IoTSystem(models.Model):
    _inherit = 'iot.system'

    output_ids = fields.One2many('iot.device.output', inverse_name='system_id')
    applies_to = fields.Selection([
        ('device', 'Device'),
        ('output', 'Output'),
    ], default='device', required=True)
