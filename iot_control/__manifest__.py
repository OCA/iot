# Copyright 2022 thingsintouch.com
# Copyright 2022 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2022 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "IoT Control",
    "version": "13.0.1.0.0",
    "category": "IoT",
    "author": "thingsintouch.com, ForgeFlow, Creu Blanca, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "summary": "IoT module for managing Control over IoT Devices",
    "depends": ["iot_template_oca"],
    "website": "https://github.com/OCA/iot",
    "data": [
        "security/ir.model.access.csv",
        "views/iot_partner_group.xml",
        "views/iot_partner.xml",
        "views/iot_control.xml",
        "views/iot_device_group.xml",
    ],
}
