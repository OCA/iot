# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class IoTCommunicationSystem(models.Model):
    _name = "iot.communication.system"
    _description = "IoT Communication System"
    # TODO: Rename it to iot.communication.system System is confusing

    name = fields.Char(required=True)
    device_ids = fields.One2many("iot.device", inverse_name="communication_system_id")
    communication_system_action_ids = fields.One2many(
        "iot.communication.system.action", inverse_name="communication_system_id"
    )
