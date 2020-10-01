from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class IotDeviceOutput(models.Model):
    _inherit = 'iot.device.output'

    amqp_exchange = fields.Char()
    amqp_routing_key = fields.Char()
    amqp_payload = fields.Char()
    amqp_host_id = fields.Many2one(
        'iot.amqp.host',
    )

    @api.constrains(
        'amqp_exchange', 'amqp_routing_key', 'amqp_host_id',
        'system_id')
    def _check_amqp(self):
        amqp_system = self.env.ref('iot_amqp.amqp_system')
        for rec in self:
            if rec.system_id == amqp_system:
                if not rec.amqp_exchange:
                    raise ValidationError(_(
                        'Exchange is required'
                    ))
                if not rec.amqp_routing_key:
                    raise ValidationError(_(
                        'Routing Key is required'
                    ))
                if not rec.amqp_host_id:
                    raise ValidationError(_(
                        'Host is required'
                    ))
