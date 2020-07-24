from odoo.tests.common import TransactionCase


class TestIotIn(TransactionCase):
    def test_device(self):
        serial = 'testingdeviceserial'
        passphrase = 'password'
        device = self.env['iot.device'].create({
            'name': 'Device',
        })
        value = '12'
        device_input = self.env['iot.device.input'].create({
            'name': 'Input',
            'device_id': device.id,
            'active': True,
            'serial': serial,
            'passphrase': passphrase,
            'call_model_id': self.ref('iot_input.model_iot_device_input'),
            'call_function': 'test_input_device'
        })
        iot = self.env['iot.device.input']
        response = iot.get_device_input(serial=serial + serial,
                                        passphrase=passphrase,
                                        value=value)
        self.assertTrue(response['status'] == 'error')

        response = iot.get_device_input(serial=serial,
                                        passphrase=passphrase + passphrase,
                                        value=value)
        self.assertTrue(response['status'] == 'error')

        iot = iot.get_device_input(
            serial=serial, passphrase=passphrase, value=value)
        args = 'hello'
        res = iot.call_device(args)
        self.assertEqual(res, {'status': 'ok', 'value': args})
        self.assertTrue(device_input.action_ids)
        self.assertEqual(device_input.action_ids.args, str(args))
        self.assertEqual(device_input.action_ids.res, str(res))

        device_input.active = False
        response2 = iot.get_device_input(
            serial=serial, passphrase=passphrase, value=value)
        self.assertTrue(response2['status'] == 'error')
