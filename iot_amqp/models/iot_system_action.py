from odoo import models


class IoTSystemAction(models.Model):
    _inherit = 'iot.system.action'

    def _run(self, device_action):
        if self != self.env.ref('iot_amqp.amqp_action'):
            return super()._run(device_action)
        device_action._run_amqp()
