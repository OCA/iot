from odoo import api, fields, models


class IotDevice(models.Model):
    _inherit = 'iot.device'

    input_ids = fields.One2many(
        'iot.device.input',
        inverse_name='device_id'
    )
    input_count = fields.Integer(compute='_compute_input_count')

    @api.depends('input_ids')
    def _compute_input_count(self):
        for r in self:
            r.input_count = len(r.input_ids)

    @api.multi
    def action_show_input(self):
        self.ensure_one()
        action = self.env.ref('iot_input.iot_device_input_action')
        result = action.read()[0]

        result['context'] = {
            'default_device_id': self.id,
        }
        result['domain'] = "[('device_id', '=', " + \
                           str(self.id) + ")]"
        if len(self.input_ids) == 1:
            result['views'] = [(False, 'form')]
            result['res_id'] = self.input_ids.id
        return result
