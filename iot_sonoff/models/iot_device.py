# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import json
from odoo import api, fields, models


class IoTDevice(models.Model):
    _inherit = 'iot.device'

    is_sonoff = fields.Boolean(store=True, compute='_compute_is_sonoff')
    state = fields.Selection(selection_add=[
        ('sonoff-on', 'On'),
        ('sonoff-off', 'Off')
    ])

    @api.multi
    @api.depends('system_id')
    def _compute_is_sonoff(self):
        sonoff = self.env.ref('iot_sonoff.iot_sonoff_system',
                              raise_if_not_found=False)
        for rec in self:
            rec.is_sonoff = rec.system_id == sonoff


class IoTDeviceAction(models.Model):
    _inherit = 'iot.device.action'

    def run_extra_actions(self, status, result):
        res = super().run_extra_actions(status, result)
        sonoff_system = self.env.ref('iot_sonoff.iot_sonoff_system')
        if status == 'ok' and self.device_id.system_id == sonoff_system:
            json_result = json.loads(result)
            self.device_id.state = 'sonoff-%s' % json_result['status']
        return res
