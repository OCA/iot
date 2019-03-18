# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestIotTemplate(TransactionCase):

    def setUp(self):
        super(TestIotTemplate, self).setUp()
        self.parent_template = self.env['iot.template'].create({
            'name': 'Parent template',
            'key_ids': [
                (0, 0, {
                    'key': 'passphrase',
                })
            ],
            'input_ids': [
                (0, 0, {
                    'name': 'INPUT 1',
                    'call_model_id': False,
                    'call_function': 'iot_ras_default_action',
                    'params': "{'serial': '${serial}', "
                              "'passphrase': '${passphrase}'}"
                })
            ],

        })
        self.template = self.env['iot.template'].create({
            'name': 'template',
            'parent_id': self.parent_template.id,
            'key_ids': [
                (0, 0, {
                    'key': 'serial2',
                }),
            ],
            'input_ids': [
                (0, 0, {
                    'name': 'INPUT 2',
                    'call_model_id': False,
                    'call_function': 'iot_ras_default_action',
                    'params': "{'serial': '${serial2}', "
                              "'passphrase': '${passphrase}'}"
                })
            ],
        })

    def test_generation(self):
        wizard = self.env['iot.device.configure'].create({})
        self.assertFalse(wizard.serial)
        wizard.run()
        self.assertTrue(wizard.serial)
        device_config = self.env['iot.device.configure'].configure(
            wizard.serial, self.template.name
        )
        device = self.env['iot.device'].search([
            ('name', '=', device_config['name'])])
        self.assertTrue(device)
        self.assertEqual(1, len(device))
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
