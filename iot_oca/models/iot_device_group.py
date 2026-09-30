# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IotDeviceGroup(models.Model):
    _name = "iot.device.group"
    _description = "Iot Group"

    name = fields.Char(required=True)
