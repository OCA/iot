# Copyright 2022 thingsintouch.com
# Copyright 2022 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2022 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PartnerIoT(models.Model):
    _name = "iot.partner"
    _description = "Person with Control on IoT Devices"

    _sql_constraints = [
        ("rfid_code_uniq", "UNIQUE(rfid_code)", "The rfid code should be unique.",)
    ]

    partner_id = fields.Many2one(
        "res.partner", "Control Holder", ondelete="cascade", required=True
    )

    name = fields.Char(required=True, related="partner_id.name")

    # rfid_code = fields.Char("RFID Card Code", copy=False, compute=)

    group_id = fields.Many2many(
        "iot.partner.group",
        column1="iot_partner_id",
        column2="iot_partner_group_id",
        string="Partner Group Definition",
    )
