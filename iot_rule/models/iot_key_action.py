# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IotKeyAction(models.Model):

    _name = "iot.key.action"
    _description = "IoT Key - Actions Log"
    _order = "timestamp DESC"

    key_id = fields.Many2one("iot.key")
    key_name = fields.Char(related="key_id.name", string="Key's Name")
    unique_virtual_key = fields.Char()
    lock_id = fields.Many2one("iot.lock", required=True)
    result = fields.Char(required=True, default="undefined")
    timestamp = fields.Datetime(
        string="Time", default=fields.Datetime.now, required=True
    )
