# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from mock import patch
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger
from odoo.exceptions import ValidationError


class TestIoT(TransactionCase):
    def setUp(self):
        super().setUp()
        self.system = self.env['iot.system'].create({
            'name': 'Testing',
        })
        self.system_2 = self.env['iot.system'].create({
            'name': 'Testing 02',
        })
        self.action = self.env['iot.system.action'].create({
            'name': 'test',
            'system_id': self.system.id,
        })
        self.action_2 = self.env['iot.system.action'].create({
            'name': 'test 02',
            'system_id': self.system_2.id,
        })
        self.device = self.env['iot.device'].create({
            'name': 'Device',
        })
        self.assertEqual(self.device.output_count, 0)
        self.output = self.env['iot.device.output'].create({
            'system_id': self.system.id,
            'device_id': self.device.id,
            'name': 'Output',
        })

    def test_views(self):
        self.assertEqual(self.device.output_count, 1)
        res = self.device.action_show_output()
        self.assertEqual(
            self.output, self.env[res['res_model']].browse(res['res_id']))

    def test_action(self):
        self.assertEqual(self.output.action_count, 0)
        with mute_logger('odoo.addons.iot.models.iot_system_action'):
            self.output.with_context(
                iot_system_action_id=self.action.id).device_run_action()
        self.assertEqual(self.output.action_count, 1)
        self.assertEqual(self.output.action_ids.status, 'failed')

    def test_action_archived_device(self):
        self.assertEqual(self.output.action_count, 0)
        self.device.active = False
        with mute_logger("odoo.addons.iot.models.iot_system_action"):
            self.output.with_context(
                iot_system_action_id=self.action.id
            ).device_run_action()
        self.assertEqual(self.output.action_count, 0)

    def test_correct_action(self):
        self.assertEqual(self.output.action_count, 0)
        with patch('odoo.addons.iot.models.iot_system_action.'
                   'IoTSystemAction._run', return_value=('ok', '')):
            self.output.with_context(
                iot_system_action_id=self.action.id).device_run_action()
        self.assertEqual(self.output.action_count, 1)
        self.assertEqual(self.output.action_ids.status, 'ok')

    def test_constrains(self):
        with self.assertRaises(ValidationError):
            self.output.with_context(
                iot_system_action_id=self.action_2.id).device_run_action()
