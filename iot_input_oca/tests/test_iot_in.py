from odoo.tests.common import TransactionCase


class TestIotIn(TransactionCase):
    def test_device(self):
        serial = 'testingdeviceserial'
        passphrase = 'password'
        device = self.env['iot.device'].create({
            'name': 'Device',
        })
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
        self.assertFalse(
            iot.get_device(serial=serial + serial, passphrase=passphrase))
        self.assertFalse(
            iot.get_device(serial=serial, passphrase=passphrase + passphrase))
        iot = iot.get_device(
            serial=serial, passphrase=passphrase)
        self.assertEqual(iot, device_input)
        args = 'hello'
        res = iot.call_device(args)
        self.assertEqual(res, {'status': 'ok', 'value': args})
        self.assertTrue(device_input.action_ids)
        self.assertEqual(device_input.action_ids.args, str(args))
        self.assertEqual(device_input.action_ids.res, str(res))

    def test_multi_input(self):
        device_identification = 'test_device_name'
        passphrase = 'password'
        device = self.env['iot.device'].create({
            'name': 'Device',
            'device_identification': device_identification,
            'passphrase': passphrase
        })
        address_1 = 'I0'
        self.env['iot.device.input'].create({
            'name': 'Input 1',
            'device_id': device.id,
            'address': address_1,
            'call_model_id': self.ref('iot_input.model_iot_device_input'),
            'call_function': 'test_model_function'
        })
        address_2 = 'I1'
        self.env['iot.device.input'].create({
            'name': 'Input 2',
            'device_id': device.id,
            'address': address_2,
            'call_model_id': self.ref('iot_input.model_iot_device_input'),
            'call_function': 'test_model_function'
        })
        single_input_values = [{'input': address_1, 'value': 'test'}]
        self.assertEqual(device.parse_multi_input(
            device_identification + device_identification, passphrase,
            single_input_values)['status'], 'error')
        self.assertEqual(device.parse_multi_input(
            device_identification, passphrase + passphrase,
            single_input_values)['status'], 'error')
        self.assertEqual(device.parse_multi_input(
            device_identification, passphrase, False)['status'], 'error')

        for response in device.parse_multi_input(
            device_identification, passphrase,
                [{'address': address_1}]):
            self.assertEqual(response['status'], 'error')
        for response in device.parse_multi_input(
            device_identification, passphrase,
                [{'address': address_1, 'uuid': 'abc'}]):
            self.assertEqual(response['status'], 'error')
            self.assertTrue('uuid' in response)

        for response in device.parse_multi_input(
            device_identification, passphrase,
                [{'value': 'test value'}]):
            self.assertEqual(response['status'], 'error')
        for response in device.parse_multi_input(
            device_identification, passphrase,
                [{'value': 'test value', 'uuid': 'abc'}]):
            self.assertEqual(response['status'], 'error')
            self.assertTrue('uuid' in response)

        non_existing_address = 'I3'
        for response in device.parse_multi_input(
            device_identification, passphrase,
                [{'address': non_existing_address,
                  'value': 'test value 1'}]):
            self.assertEqual(response['status'], 'error')
        for response in device.parse_multi_input(
            device_identification, passphrase,
                [{'address': non_existing_address,
                  'value': 'test value 1',
                  'uuid': 'abc'}]):
            self.assertEqual(response['status'], 'error')
            self.assertTrue('uuid' in response)

        for response in device.parse_multi_input(
            device_identification, passphrase,
                [{'address': address_1, 'value': 'test'}]):
            self.assertEqual(response['status'], 'ok')
        for response in device.parse_multi_input(
            device_identification, passphrase,
                [{'address': address_1, 'value': 'test value 1'},
                 {'address': address_1, 'value': 'test value 2'}]):
            self.assertEqual(response['status'], 'ok')
        for response in device.parse_multi_input(
            device_identification, passphrase,
                [{'address': address_1, 'value': 'test value 1'},
                 {'address': address_2, 'value': 'test value 2'}]):
            self.assertEqual(response['status'], 'ok')
        for response in device.parse_multi_input(
            device_identification, passphrase,
                [{'address': address_1, 'value': 'test value 1'},
                 {'address': address_1, 'value': 'test value 2'},
                 {'address': address_2, 'value': 'test value 3'}]):
            self.assertEqual(response['status'], 'ok')
        response_with_uuid = [
            {'address': address_1, 'value': 'test value 1', 'uuid': 'abc'},
            {'address': address_1, 'value': 'test value 2', 'uuid': 'def'},
            {'address': address_2, 'value': 'test value 3', 'uuid': 'ghi'}
        ]
        for response in device.parse_multi_input(
            device_identification, passphrase,
                response_with_uuid):
            self.assertTrue(response['uuid'])
            self.assertEqual(
                response['message'],
                [x for x in response_with_uuid if x['uuid'] == response['uuid']][0]
            )

        # Test for address passed as number
        address_3 = 3
        self.env['iot.device.input'].create({
            'name': 'Input 1',
            'device_id': device.id,
            'address': address_3,
            'call_model_id': self.ref('iot_input.model_iot_device_input'),
            'call_function': 'test_model_function'
        })
        for response in device.parse_multi_input(
            device_identification, passphrase,
                [{'address': address_3, 'value': 12.3}]):
            self.assertEqual(response['status'], 'ok')

        device.active = False
        self.assertEqual(device.parse_multi_input(
            device_identification, passphrase,
            [{'address': address_1, 'value': 'test'}])['status'], 'error')
