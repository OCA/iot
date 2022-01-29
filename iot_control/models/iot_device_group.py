# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IotDeviceGroup(models.Model):
    _inherit = "iot.device.group"

    control_ids = fields.Many2many(
        "iot.control",
        column1="iot_device_group_id",
        column2="iot_control_id",
        string="Device Control Rules",
    )
