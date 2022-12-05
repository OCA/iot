# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'IoT Input',
    'version': '12.0.1.4.2',
    'category': 'IoT',
    'author': "Creu Blanca, "
              "Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'installable': True,
    'summary': 'IoT Input module',
    "website": "https://github.com/OCA/iot",
    'depends': [
        'iot_output',
        'iot',
        'mail',
    ],
    # odoo_test_helper is needed for the tests
    'maintainers': ['etobella'],
    'data': [
        'security/ir.model.access.csv',
        'views/iot_device_views.xml',
        'views/iot_device_input_views.xml',
    ],
}
