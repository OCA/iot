# Copyright 2022 thingsintouch.com
# Copyright 2022 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2022 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class IotControlType(models.Model):
    _name = "iot.control.type"
    _description = "Type of Control of an IoT Rule"

    _sql_constraints = [("unique_code", "UNIQUE(code)", "Code must be unique")]

    name = fields.Char(
        String="Type of Control",
        help="Type of Control given to a Group of Persons by an IoT Rule over a Group of Devices",
        required=True,
        index=True,
    )
    code = fields.Char("IoT Control Code")
