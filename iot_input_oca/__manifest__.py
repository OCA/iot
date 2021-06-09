# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "IoT Input",
    "version": "13.0.1.0.0",
    "category": "IoT",
    "author": "Creu Blanca, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "summary": "IoT Input module",
    "depends": ["iot_output_oca", "mail"],
    "website": "https://github.com/OCA/iot",
    "maintainers": ["etobella"],
    "data": [
        "security/ir.model.access.csv",
        "views/iot_device_views.xml",
        "views/iot_device_input_views.xml",
    ],
}
