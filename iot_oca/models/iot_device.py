# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class IoTDevice(models.Model):
    _name = "iot.device"
    _description = "IoT Device"

    name = fields.Char(required=True)
    system_id = fields.Many2one("iot.system", required=True)
    action_ids = fields.One2many("iot.device.action", inverse_name="device_id")
    active = fields.Boolean(default=True)
    device_identification = fields.Char()
    passphrase = fields.Char()
    # TODO: On 14 remove passpharse and device_identification.
    #  Create a multiparameter input in order to manage this
    state = fields.Selection([], readonly=True)
    model = fields.Char()
    ip = fields.Char()
    action_count = fields.Integer(compute="_compute_action_count")
    group_id = fields.Many2one("iot.device.group")
    tag_ids = fields.Many2many("iot.device.tag")
    color = fields.Integer()

    @api.depends("action_ids")
    def _compute_action_count(self):
        for record in self:
            record.action_count = len(record.action_ids)

    def device_run_action(self):
        system_action = self.env["iot.system.action"].browse(
            self.env.context.get("iot_system_action_id")
        )
        for rec in self:
            action = self.env["iot.device.action"].create(
                {"device_id": rec.id, "system_action_id": system_action.id}
            )
            action.run()
