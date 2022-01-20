# Copyright 2022 thingsintouch.com
# Copyright 2022 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2022 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class IotControl(models.Model):
    _name = "iot.control"
    _description = "Manage Control over IoT Devices"
    _order = "name"

    name = fields.Char(required=True)

    partner_control_ids = fields.Many2many(
        "res.partner", column1="iot_control_id", column2="partner_id", string="Partners"
    )
