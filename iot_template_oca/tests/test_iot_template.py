# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import HttpCase


class TestIotTemplate(HttpCase):
    def setUp(self):
        super(TestIotTemplate, self).setUp()
        self.system = self.env["iot.system"].create({"name": "Testing"})
        self.system_2 = self.env["iot.system"].create({"name": "Testing 2"})
        self.parent_template = self.env["iot.template"].create(
            {
                "name": "Parent template",
                "key_ids": [(0, 0, {"key": "passphrase"})],
                "input_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "INPUT 1",
                            "call_model_id": False,
                            "call_function": "iot_ras_default_action",
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
        self.template = self.env["iot.template"].create(
            {
                "name": "template",
                "parent_id": self.parent_template.id,
                "key_ids": [(0, 0, {"key": "serial2"})],
                "input_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "INPUT 2",
                            "call_model_id": False,
                            "call_function": "iot_ras_default_action",
                            "params": "{'serial': '${serial2}', "
                            "'passphrase': '${passphrase}'}",
                        },
                    )
                ],
                "output_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "OUTPUT 2",
                            "system_id": self.system_2.id,
                            "params": "{'ip': '1234'}",
                        },
                    )
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
        self.assertEqual(2, len(device.output_ids))
        self.assertEqual(2, len(device.input_ids))
        input1 = device.input_ids.filtered(
            lambda r: r.template_input_id == self.parent_template.input_ids
        )
        self.assertTrue(input1)
        input2 = device.input_ids.filtered(
            lambda r: r.template_input_id == self.template.input_ids
        )
        self.assertTrue(input2)
        self.assertNotEqual(input1, input2)
        self.assertGreater(len(input1.passphrase), 0)
        self.assertGreater(len(input2.passphrase), 0)
        self.assertEqual(input1.passphrase, input2.passphrase)
        self.assertGreater(len(input1.serial), 0)
        self.assertGreater(len(input2.serial), 0)
        self.assertNotEqual(input1.serial, input2.serial)
        output1 = device.output_ids.filtered(
            lambda r: r.template_output_id == self.parent_template.output_ids
        )
        self.assertTrue(output1)
        output2 = device.output_ids.filtered(
            lambda r: r.template_output_id == self.template.output_ids
        )
        self.assertTrue(output2)
        self.assertNotEqual(output1, output2)
        self.assertEqual(output1.system_id, self.system)
        self.assertFalse(output1.ip)
        self.assertEqual(output2.system_id, self.system_2)
        self.assertEqual(output2.ip, "1234")

    def test_missing_configuration(self):
        wizard = self._get_wizard()
        url = wizard.url.replace(wizard.serial, wizard.serial + wizard.serial)
        device_config = self.url_open(url, data={"template": self.template.name}).json()
        self.assertFalse(device_config)

    def test_no_double_configuration(self):
        """
        We expect that it is not allowed to do the same call twice,
        the first it must work properly.
        No result should be returned on the second one
        """
        wizard = self._get_wizard()
        url = wizard.url
        device_config = self.url_open(url, data={"template": self.template.name}).json()
        self.assertTrue(device_config)
        device = self.env["iot.device"].search([("name", "=", device_config["name"])])
        self.assertTrue(device)
        device_config = self.url_open(url, data={"template": self.template.name}).json()
        self.assertFalse(device_config)

    def test_constrain_hierarchy(self):
        with self.assertRaises(UserError):
            self.parent_template.parent_id = self.template
