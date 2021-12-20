# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "IoT Templates",
    "version": "14.0.1.0.0",
    "category": "IoT",
    "author": "Creu Blanca, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "summary": "IoT module for managing templates",
    "depends": ["iot_input_oca", "iot_output_oca"],
    "website": "https://github.com/OCA/iot",
    "data": [
        "security/ir.model.access.csv",
        "wizards/iot_device_configure.xml",
        "views/iot_template_views.xml",
    ],
    "demo": ["demo/iot_template.xml"],
}
