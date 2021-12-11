# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "IoT AMQP",
    "version": "13.0.1.1.0",
    "category": "IoT",
    "author": "Creu Blanca, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "summary": "Integrate Iot Outputs with AMQP",
    "depends": ["iot_output_oca"],
    "external_dependencies": {"python": ["pika"]},
    "website": "https://github.com/OCA/iot",
    "data": [
        "security/ir.model.access.csv",
        "views/iot_amqp_host.xml",
        "data/system_data.xml",
        "views/iot_device_output_views.xml",
    ],
}
