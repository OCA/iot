# Copyright 2022 thingsintouch.com
# Copyright 2022 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2022 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class IotControl(models.Model):
    _name = "iot.control"
    _description = "Control Rule over IoT Devices"
    _order = "name"

    name = fields.Char(required=True)

    partner_group_ids = fields.Many2many(
        "iot.partner.group",
        column1="iot_control_id",
        column2="iot_partner_group_id",
        string="Group of Persons",
    )

    device_group_ids = fields.Many2many(
        "iot.device.group",
        column1="iot_control_id",
        column2="iot_device_group_id",
        string="Group of Devices",
    )

    control_type_ids = fields.Many2many(
        comodel_name="iot.control.type",
        string="Control Given",
        help="Specifies which types of Control are given on this Rule",
    )
