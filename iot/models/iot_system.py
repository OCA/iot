# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class IoTSystem(models.Model):
    _name = "iot.system"
    _description = "IoT System"
    # TODO: Rename it to iot.communication.system System is confusing

    name = fields.Char(required=True)
    device_ids = fields.One2many('iot.device', inverse_name='system_id')
    system_action_ids = fields.One2many(
        'iot.system.action', inverse_name='system_id'
    )
