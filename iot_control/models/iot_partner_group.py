# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IotPartnerGroup(models.Model):
    _name = "iot.partner.group"
    _description = "Iot Group of Persons"

    name = fields.Char(string="Name of the Group", required=True)

    iot_partner_ids = fields.Many2many(
        "iot.partner",
        column1="iot_partner_group_id",
        column2="iot_partner_id",
        string="Persons in this Group",
    )

    control_ids = fields.Many2many(
        "iot.control",
        column1="iot_partner_id",
        column2="iot_control_id",
        string="Device Control Rules",
    )
