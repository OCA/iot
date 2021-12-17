# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class IoTDevice(models.Model):
    _name = "iot.device"
    _description = "IoT Device"
    _inherit = "image.mixin"

    name = fields.Char(required=True)
    communication_system_id = fields.Many2one("iot.communication.system", required=True)
    action_ids = fields.One2many("iot.device.action", inverse_name="device_id")
    active = fields.Boolean(default=True)
    state = fields.Selection([], readonly=True)
    model = fields.Char()
    ip = fields.Char(string="IP")
    action_count = fields.Integer(compute="_compute_action_count")
    group_id = fields.Many2one("iot.device.group")
    tag_ids = fields.Many2many("iot.device.tag")
    color = fields.Integer()
    last_contact_date = fields.Datetime(readonly=True)
    icon = fields.Selection(
        [
            ("fa fa-television fa-4x", "television"),
            ("fa fa-wifi fa-4x", "wifi"),
            ("fa fa-laptop fa-4x", "laptop"),
            ("fa fa-desktop fa-4x", "desktop"),
            ("fa fa-archive fa-4x", "archive"),
            ("fa fa-mobile fa-6x", "mobile"),
        ],
        "Icon",
    )

    @api.depends("action_ids")
    def _compute_action_count(self):
        for record in self:
            record.action_count = len(record.action_ids)

    def device_run_action(self):
        system_action = self.env["iot.communication.system.action"].browse(
            self.env.context.get("iot_communication_system_action_id")
        )
        for rec in self:
            action = self.env["iot.device.action"].create(
                {
                    "device_id": rec.id,
                    "communication_system_action_id": system_action.id,
                }
            )
            action.run()
