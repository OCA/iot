# Copyright 2020 Dimitrios Tanis (dtanis@tanisfood.gr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Iot Events",
    "summary": "Describe and Log IoT Events",
    "version": "12.0.1.0.0",
    "category": "IoT",
    "website": "https://github.com/OCA/iot",
    "author": "Dimitrios Tanis, "
              "Odoo Community Association (OCA)",
    "maintainers": ["diggy128"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "iot_input", "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/iot_event_data.xml",
        "data/iot_event_mail.xml",
        "views/iot_event_view.xml",
        "views/iot_device_input_view.xml",
        "views/iot_device_view.xml",
    ],
}
