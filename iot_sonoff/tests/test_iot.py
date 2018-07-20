# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from mock import patch
from odoo.tests.common import TransactionCase


class TestingResultOn(object):
    text = '{"status" : "on"}'

    def raise_for_status(self):
        return


class TestingResultOff(object):
    text = '{"status" : "off"}'

    def raise_for_status(self):
        return


class TestIoT(TransactionCase):
    def setUp(self):
        super().setUp()
        self.system = self.browse_ref('iot_sonoff.iot_sonoff_system')
        self.on = self.browse_ref('iot_sonoff.iot_sonoff_action_on')
        self.off = self.browse_ref('iot_sonoff.iot_sonoff_action_off')
        self.check = self.browse_ref('iot_sonoff.iot_sonoff_action_status')
        self.device = self.env['iot.device'].create({
            'name': 'Device',
            'system_id': self.system.id,
            'ip': 'testing',
        })

    def test_compute(self):
        self.assertTrue(self.device.is_sonoff)
        system_2 = self.env['iot.system'].create({
            'name': 'Testing 02',
        })
        device_2 = self.env['iot.device'].create({
            'name': 'Device',
            'system_id': system_2.id,
        })
        self.assertFalse(device_2.is_sonoff)

    def test_correct_action(self):
        self.assertEqual(self.device.action_count, 0)
        with patch('requests.get', return_value=TestingResultOn()):
            self.device.with_context(
                iot_system_action_id=self.on.id).device_run_action()
        self.assertEqual(self.device.state, 'sonoff-on')
        self.assertEqual(self.device.action_count, 1)
        with patch('requests.get', return_value=TestingResultOff()):
            self.device.with_context(
                iot_system_action_id=self.off.id).device_run_action()
        self.assertEqual(self.device.state, 'sonoff-off')
        self.assertEqual(self.device.action_count, 2)
        with patch('requests.get', return_value=TestingResultOff()):
            self.device.with_context(
                iot_system_action_id=self.check.id).device_run_action()
        self.assertEqual(self.device.state, 'sonoff-off')
        self.assertEqual(self.device.action_count, 3)
