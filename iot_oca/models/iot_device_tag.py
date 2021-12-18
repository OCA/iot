# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IotDeviceTag(models.Model):

    _name = "iot.device.tag"
    _description = "Device Tag"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color Index")
