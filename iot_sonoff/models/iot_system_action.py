# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models
import requests


class IoTSystemAction(models.Model):
    _inherit = 'iot.system.action'

    def _run_sonoff(self, device_action, action):
        request = requests.get(
            'http://%s/%s' % (device_action.device_id.ip, action)
        )
        request.raise_for_status()
        return request.text

    def _run(self, device_action):
        if self == self.env.ref('iot_sonoff.iot_sonoff_action_on'):
            return self._run_sonoff(device_action, 'on')
        if self == self.env.ref('iot_sonoff.iot_sonoff_action_off'):
            return self._run_sonoff(device_action, 'off')
        return super()._run(device_action)
