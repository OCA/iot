# Copyright 2022 thingsintouch.com
# Copyright 2022 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2022 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PartnerControl(models.Model):

    _inherit = "res.partner"

    _sql_constraints = [
        (
            "rfid_code_uniq",
            "UNIQUE(rfid_code)",
            "The rfid code should be unique.",
        )
    ]

    rfid_code = fields.Char("RFID Card Code", copy=False)

    # control_ids = fields
