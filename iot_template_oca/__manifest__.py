# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "IoT Templates",
    "version": "16.0.1.0.1",
    "author": "Creu Blanca, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "IoT",
    "installable": True,
    "application": True,
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
