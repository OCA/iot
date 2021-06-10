from odoo import api, models


class IotDeviceInput(models.Model):
    _inherit = "iot.device.input"

    @api.model
    def iot_ras_default_action(self, message):
        return {"action_msg": message, "action": "check_in"}
