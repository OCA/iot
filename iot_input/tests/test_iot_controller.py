import json

from odoo.tests.common import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestIotController(HttpCase):
    def setUp(self):
        super().setUp()
        self.device_identification = "test_device_name"
        self.passphrase = "password"
        self.device = self.env["iot.device"].create(
            {
                "name": "Device",
                "device_identification": self.device_identification,
                "passphrase": self.passphrase,
            }
        )
        self.address_1 = "I0"
        self.serial = "testingdeviceserial"
        self.input_passphrase = "password"
        self.device_input_1 = self.env["iot.device.input"].create(
            {
                "name": "Input 1",
                "device_id": self.device.id,
                "address": self.address_1,
                "serial": self.serial,
                "passphrase": self.input_passphrase,
                "call_model_id": self.env.ref(
                    "iot_input.model_iot_device_input"
                ).id,
                "call_function": "test_model_function",
            }
        )
        self.address_2 = "I1"
        self.env["iot.device.input"].create(
            {
                "name": "Input 2",
                "device_id": self.device.id,
                "address": self.address_2,
                "call_model_id": self.env.ref(
                    "iot_input.model_iot_device_input"
                ).id,
                "call_function": "test_model_function",
            }
        )
        self.single_input_values = [{"input": self.address_1, "value": "test"}]
        self.values = json.dumps(
            [
                {"address": self.address_1, "value": "test value 1"},
                {
                    "address": self.address_1,
                    "value": 2.3,
                },  # Checking that nothing wrong happens with a non string
                {"address": self.address_2, "value": "test value 3"},
            ]
        )

    def test_single_controller(self):
        res = self.url_open(
            "/iot/%s/action" % self.serial,
            data={"passphrase": self.input_passphrase, "value": "123"},
        )
        self.assertEqual(res.json()["status"], "ok")

    def test_single_controller_archived_device(self):
        self.device.write({"active": False})
        res = self.url_open(
            "/iot/%s/action" % self.serial,
            data={"passphrase": self.input_passphrase, "value": "123"},
        )
        self.assertEqual(res.json()["status"], "error")

    def test_multi_input_controller_error_passphrase(self):
        res = self.url_open(
            "/iot/%s/multi_input" % self.device_identification,
            data={"values": self.values},
        ).json()
        self.assertEqual(res["status"], "error")

    def test_multi_input_controller_error_values(self):
        res = self.url_open(
            "/iot/%s/multi_input" % self.device_identification,
            data={"passphrase": self.passphrase},
        ).json()
        self.assertEqual(res["status"], "error")

    def test_multi_input_controller_syntax_error(self):
        res = self.url_open(
            "/iot/%s/multi_input" % self.device_identification,
            data={"passphrase": self.passphrase, "values": "{}"},
        ).json()
        self.assertEqual(res["status"], "error")

    def test_multi_input_controller_malformed_error(self):
        res = self.url_open(
            "/iot/%s/multi_input" % self.device_identification,
            data={"passphrase": self.passphrase, "values": "{1234}"},
        ).json()
        self.assertEqual(res["status"], "error")

    def test_multi_input_controller(self):
        res = self.url_open(
            "/iot/%s/multi_input" % self.device.device_identification,
            data={"passphrase": self.passphrase, "values": self.values},
        )
        result = res.json()
        for response in result:
            self.assertEqual(response["status"], "ok")

    def test_multi_input_controller_unauthorized_iot_exists(self):
        res = self.url_open(
            "/iot/%s/check" % self.serial, data={"passphrase": self.input_passphrase}
        ).json()
        self.assertEqual(res["state"], True)

    def test_multi_input_controller_unauthorized_iot_no_exists(self):
        res = self.url_open(
            "/iot/%s/check" % self.passphrase,
            data={"passphrase": self.input_passphrase},
        ).json()
        self.assertEqual(res["state"], False)
