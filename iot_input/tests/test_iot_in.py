import json
from odoo.tests.common import TransactionCase


class TestIotIn(TransactionCase):
    def test_device(self):
        serial = 'testingdeviceserial'
        passphrase = 'password'
        device = self.env['iot.device'].create({
            'name': 'Device',
        })
        input = self.env['iot.device.input'].create({
            'name': 'Input',
            'device_id': device.id,
            'active': True,
            'serial': serial,
            'passphrase': passphrase,
            'call_model_id': self.ref('iot_input.model_iot_device_input'),
            'call_function': 'test_input_device'
        })
        iot = self.env['iot.device.input']
        json_response = json.loads(iot.get_device(serial=serial + serial, passphrase=passphrase))
        self.assertTrue(json_response['status'] == 'error')

        json_response2 = json.loads(iot.get_device(serial=serial, passphrase=passphrase + passphrase))
        self.assertTrue(json_response2['status'] == 'error')

        iot = iot.get_device(
            serial=serial, passphrase=passphrase)
        self.assertEqual(iot, input)
        args = 'hello'
        res = iot.call_device(args)
        self.assertEqual(res, {'status': 'ok', 'value': args})
        self.assertTrue(input.action_ids)
        self.assertEqual(input.action_ids.args, str(args))
        self.assertEqual(input.action_ids.res, str(res))
