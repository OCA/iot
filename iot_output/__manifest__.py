# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'IoT Output',
    'version': '12.0.1.1.1',
    'category': 'IoT',
    'author': "Creu Blanca, "
              "Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'summary': 'IoT allow multiple outputs',
    "website": "https://github.com/OCA/iot",
    'depends': [
        'iot',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/iot_device_output_views.xml',
        'views/iot_device_views.xml',
    ],
}
