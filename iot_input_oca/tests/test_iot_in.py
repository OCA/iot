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
            'serial': serial,
            'passphrase': passphrase,
            'call_model_id': self.ref('iot_input.model_iot_device_input'),
            'call_function': 'test_input_device'
        })
        iot = self.env['iot.device.input']
        self.assertFalse(
            iot.get_device(serial=serial + serial, passphrase=passphrase))
        self.assertFalse(
            iot.get_device(serial=serial, passphrase=passphrase + passphrase))
        iot = iot.get_device(
            serial=serial, passphrase=passphrase)
        self.assertEqual(iot, input)
        args = 'hello'
        res = iot.call_device(args)
        self.assertEqual(res, {'status': 'ok', 'value': args})
        self.assertTrue(input.action_ids)
        self.assertEqual(input.action_ids.args, str(args))
        self.assertEqual(input.action_ids.res, str(res))
