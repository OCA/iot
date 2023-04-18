from odoo import models


class IoTCommunicationSystemAction(models.Model):
    _inherit = "iot.communication.system.action"

    def _run(self, device_action):
        if self != self.env.ref("iot_amqp_oca.amqp_action"):
            return super()._run(device_action)
        device_action._run_amqp()
