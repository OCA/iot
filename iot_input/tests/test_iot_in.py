from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestIotIn(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.serial = "testingdeviceserial"
        cls.passphrase = "password"
        cls.device = cls.env["iot.device"].create({"name": "Device"})
        cls.device_input = cls.env["iot.device.input"].create(
            {
                "name": "Input",
                "device_id": cls.device.id,
                "active": True,
                "serial": cls.serial,
                "passphrase": cls.passphrase,
                "call_model_id": cls.env.ref("iot_input.model_iot_device_input").id,
                "call_function": "test_input_device",
            }
        )
        cls.iot = cls.env["iot.device.input"]

    def test_device_action_count_ids(self):
        self.assertEqual(self.device.input_count, 1)

    def _get_devices(self):
        action = self.device.action_show_input()
        devices = self.env[action["res_model"]]
        if action["res_id"]:
            devices = devices.browse(action["res_id"])
        else:
            devices = devices.search(action["domain"])
        return devices

    def test_device_action(self):
        devices = self._get_devices()
        self.assertEqual(devices, self.device_input)
        device_input_02 = self.env["iot.device.input"].create(
            {
                "name": "Input",
                "device_id": self.device.id,
                "active": True,
                "serial": self.serial + self.serial,
                "passphrase": self.passphrase,
                "call_model_id": self.env.ref(
                    "iot_input.model_iot_device_input"
                ).id,
                "call_function": "test_input_device",
            }
        )
        devices = self._get_devices()
        self.assertIn(self.device_input, devices)
        self.assertIn(device_input_02, devices)

    def test_device_error_wrong_serial(self):
        self.assertFalse(
            self.iot.get_device(
                serial=self.serial + self.serial, passphrase=self.passphrase
            )
        )

    def test_device_error_wrong_passphrase(self):
        self.assertFalse(
            self.iot.get_device(
                serial=self.serial, passphrase=self.passphrase + self.passphrase
            )
        )

    def test_device_error_archived(self):
        self.device_input.active = False
        self.assertFalse(
            self.iot.get_device(serial=self.serial, passphrase=self.passphrase)
        )

    def test_device_error_missing_data(self):
        with self.assertRaises(ValidationError):
            self.iot.get_device(serial=None, passphrase=self.passphrase)

    def test_error_execution_without_device(self):
        res = self.iot.call_device(value="hello")
        self.assertEqual(res["status"], "error")

    def test_device_input_calling(self):
        iot = self.iot.get_device(serial=self.serial, passphrase=self.passphrase)
        self.assertEqual(iot, self.device_input)
        self.assertEqual(0, self.device_input.action_count)
        args = "hello"
        res = iot.call_device(value=args)
        self.assertEqual(res, {"status": "ok", "value": args})
        self.assertTrue(self.device_input.action_ids)
        self.assertEqual(self.device_input.action_ids.args, str([args]))
        self.assertEqual(self.device_input.action_ids.res, str(res))
        self.assertEqual(1, self.device_input.action_count)
