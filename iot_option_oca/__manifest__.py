# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Iot Custom Field Oca",
    "summary": """
        Allow to define custom field for IoT""",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "author": "Creu Blanca,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/iot",
    "depends": ["iot_template_oca"],
    "data": [
        "security/ir.model.access.csv",
        "views/iot_device_property.xml",
        "views/iot_template.xml",
        "views/iot_device.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "iot_option_oca/static/src/js/iot_option_renderer.js",
            "iot_option_oca/static/src/js/iot_option_view.js",
            "iot_option_oca/static/src/js/relational_fields.js",
            "iot_option_oca/static/src/scss/iot_option.scss",
        ],
        "web.assets_qweb": ["iot_option_oca/static/src/xml/iot_option_item.xml"],
    },
}
