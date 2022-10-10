# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "IoT Rule",
    "summary": """
        Define IoT Rules (Keys that control Inputs)""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca,ForgeFlow,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/iot",
    "depends": ["iot_input_oca"],
    "data": [
        "wizards/iot_key_wizard.xml",
        "security/ir.model.access.csv",
        "views/iot_rule.xml",
        "views/iot_key.xml",
        "views/iot_key_action.xml",
        "views/iot_lock.xml",
        "views/res_partner.xml",
        "views/iot_device_input.xml",
    ],
    "demo": [
        "demo/iot_rule_demo.xml",
        "demo/iot_lock_demo.xml",
        "demo/iot_key_demo.xml",
    ],
}
