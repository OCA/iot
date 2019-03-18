# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class IoTDevice(models.Model):
    _inherit = 'iot.device'

    output_ids = fields.One2many(
        'iot.device.output',
        inverse_name='device_id'
    )
    output_count = fields.Integer(compute='_compute_output_count')
    system_id = fields.Many2one(required=False)

    @api.multi
    @api.depends('output_ids')
    def _compute_output_count(self):
        for record in self:
            record.output_count = len(record.output_ids)

    @api.multi
    def action_show_output(self):
        self.ensure_one()
        action = self.env.ref(
            'iot_output.iot_device_output_action')
        result = action.read()[0]

        result['context'] = {
            'default_device_id': self.id,
        }
        result['domain'] = "[('device_id', '=', " + \
                           str(self.id) + ")]"
        if len(self.output_ids) == 1:
            result['views'] = [(False, 'form')]
            result['res_id'] = self.output_ids.id
        return result
