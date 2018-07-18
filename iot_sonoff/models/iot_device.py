# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
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
        sonoff = self.env.ref('iot_sonoff.iot_sonoff_system')
        for rec in self:
            rec.is_sonoff = (rec.system_id == sonoff)


class IoTDeviceAction(models.Model):
    _inherit = 'iot.device.action'

    def run_extra_actions(self, status, result):
        res = super().run_extra_actions(status, result)
        sonoff_on = self.env.ref('iot_sonoff.iot_sonoff_action_on')
        sonoff_off = self.env.ref('iot_sonoff.iot_sonoff_action_off')
        if status == 'ok' and self.system_action_id == sonoff_on:
            self.device_id.state = 'sonoff-on'
        if status == 'ok' and self.system_action_id == sonoff_off:
            self.device_id.state = 'sonoff-off'
        return res
