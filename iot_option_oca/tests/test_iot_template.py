# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase


class TestIotTemplate(HttpCase):
    def setUp(self):
        super(TestIotTemplate, self).setUp()
        self.system = self.env["iot.system"].create({"name": "Testing"})
        self.system_2 = self.env["iot.system"].create({"name": "Testing 2"})
        self.property = self.env["iot.device.property"].create(
            {"name": "Prop1", "tech_name": "prop_1", "widget": "char"}
        )
        self.action_property = self.env["iot.device.property"].create(
            {
                "name": "Prop2",
                "tech_name": "prop_2",
                "widget": "boolean",
                "is_action": True,
            }
        )
        self.template = self.env["iot.template"].create(
            {
                "name": "Parent template",
                "key_ids": [(0, 0, {"key": "passphrase"})],
                "property_ids": [(4, self.property.id), (4, self.action_property.id)],
                "input_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "INPUT 1",
                            "call_model_id": False,
                            "call_function": "get_options",
                            "params": "{'serial': '${serial}', "
                            "'passphrase': '${passphrase}'}",
                        },
                    )
                ],
                "output_ids": [
                    (0, 0, {"name": "OUTPUT 1", "system_id": self.system.id},)
                ],
            }
        )

    def _get_wizard(self):
        wizard = self.env["iot.device.configure"].create({})
        self.assertTrue(wizard.serial)
        self.assertTrue(wizard.url)
        return wizard

    def test_generation(self):
        wizard = self._get_wizard()
        device_config = self.url_open(
            wizard.url, data={"template": self.template.name}
        ).json()
        device = self.env["iot.device"].search([("name", "=", device_config["name"])])
        self.assertTrue(device)
        self.assertEqual(1, len(device))
        self.assertEqual(1, len(device.input_ids))
        self.assertEqual(2, len(device.option_ids))
        option = device.option_ids.filtered(lambda r: r.property_id == self.property)
        self.assertTrue(option)
        option.value = "Hello"
        input1 = device.input_ids.filtered(
            lambda r: r.template_input_id == self.template.input_ids
        )
        self.assertTrue(input1)
        res = self.url_open(
            "/iot/%s/action" % input1.serial, data={"passphrase": input1.passphrase},
        )
        json_res = res.json()
        self.assertEqual(json_res["status"], "ok")
        self.assertEqual(json_res["prop_2"], False)
        self.assertEqual(json_res["prop_1"], "Hello")
        option = device.option_ids.filtered(
            lambda r: r.property_id == self.action_property
        )
        self.assertTrue(option)
        option.value = True
        res = self.url_open(
            "/iot/%s/action" % input1.serial, data={"passphrase": input1.passphrase},
        )
        json_res = res.json()
        self.assertEqual(json_res["status"], "ok")
        self.assertEqual(json_res["prop_2"], True)
        self.assertEqual(json_res["prop_1"], "Hello")
        res = self.url_open(
            "/iot/%s/action" % input1.serial, data={"passphrase": input1.passphrase},
        )
        json_res = res.json()
        self.assertEqual(json_res["status"], "ok")
        self.assertEqual(json_res["prop_2"], False)
        self.assertEqual(json_res["prop_1"], "Hello")
