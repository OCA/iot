# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'IoT Base',
    'version': '12.0.1.3.1',
    'category': 'IoT',
    'author': "Creu Blanca, "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/iot",
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'summary': 'IoT base module',
    'depends': [
        'base',
    ],
    'data': [
        'security/iot_security.xml',
        'security/ir.model.access.csv',
        'views/iot_menu.xml',
        "views/iot_device_tag.xml",
        "views/iot_device_group.xml",
        'views/iot_system_views.xml',
        'views/iot_device_views.xml',
    ],
}
