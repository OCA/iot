# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class IoTDeviceAction(models.Model):
    _name = 'iot.device.action'
    _description = 'IoT Action'
    _order = 'date_ok desc'

    device_id = fields.Many2one('iot.device', required=True, readonly=True)
    system_action_id = fields.Many2one('iot.system.action', required=True)
    status = fields.Selection([
        ('ok', 'Ok'),
        ('pending', 'Pending'),
        ('failed', 'Failed')
    ], required=True, default='pending')
    result = fields.Text()
    date_ok = fields.Datetime(readonly=True, string="Ok date")

    @api.multi
    @api.constrains('device_id', 'system_action_id')
    def _check_system(self):
        if self.filtered(
            lambda r: r.device_id.system_id != r.system_action_id.system_id
        ):
            raise ValidationError(_(
                'Device and action must be of the same system'))

    def run_extra_actions(self, status, result):
        return

    @api.multi
    def run(self):
        self.ensure_one()
        if self.status != 'ok':
            status, result = self.system_action_id.run(self)
            self.write({
                'status': status,
                'result': result,
                'date_ok': fields.Datetime.now() if status == 'ok' else False,
            })
            self.run_extra_actions(status, result)
