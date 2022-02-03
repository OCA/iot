from odoo.tests.common import SavepointCase
from odoo.tools import mute_logger


class TestIotIn(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.device_identification = "test_device_name"
        cls.passphrase = "password"
        cls.device = cls.env["iot.device"].create(
            {
                "name": "Device",
                "device_identification": cls.device_identification,
                "passphrase": cls.passphrase,
            }
        )
        cls.address_1 = "I0"
        cls.device_input_1 = cls.env["iot.device.input"].create(
            {
                "name": "Input 1",
                "device_id": cls.device.id,
                "address": cls.address_1,
                "call_model_id": cls.env.ref("iot_input.model_iot_device_input").id,
                "call_function": "test_model_function",
            }
        )
        cls.address_2 = "I1"
        cls.env["iot.device.input"].create(
            {
                "name": "Input 2",
                "device_id": cls.device.id,
                "address": cls.address_2,
                "call_model_id": cls.env.ref("iot_input.model_iot_device_input").id,
                "call_function": "test_model_function",
            }
        )
        cls.single_input_values = [{"input": cls.address_1, "value": "test"}]

    def test_multi_input_error_wrong_identification(self):
        self.assertEqual(
            self.env["iot.device"].parse_multi_input(
                self.device_identification + self.device_identification,
                self.passphrase,
                self.single_input_values,
            )["status"],
            "error",
        )

    def test_multi_input_error_wrong_passphrase(self):
        self.assertEqual(
            self.env["iot.device"].parse_multi_input(
                self.device_identification,
                self.passphrase + self.passphrase,
                self.single_input_values,
            )["status"],
            "error",
        )

    def test_multi_input_error_no_inputs(self):
        self.assertEqual(
            self.env["iot.device"].parse_multi_input(
                self.device_identification, self.passphrase, False
            )["status"],
            "error",
        )

    def test_multi_input_non_existing_address(self):
        non_existing_address = "I3"
        for response in self.env["iot.device"].parse_multi_input(
            self.device_identification,
            self.passphrase,
            [{"address": non_existing_address, "value": "test value 1"}],
        ):
            self.assertEqual(response["status"], "error")

    @mute_logger("odoo.addons.iot_input.models.iot_device_input")
    def test_error_missing_parameter(self):
        for response in self.env["iot.device"].parse_multi_input(
            self.device_identification, self.passphrase, [{"address": self.address_1}]
        ):
            self.assertEqual(response["status"], "ko")

    @mute_logger("odoo.addons.iot_input.models.iot_device_input")
    def test_error_with_extra_args(self):
        for response in self.env["iot.device"].parse_multi_input(
            self.device_identification,
            self.passphrase,
            [{"address": self.address_1, "uuid": "abc"}],
        ):
            self.assertEqual(response["status"], "ko")
            self.assertTrue("uuid" in response)

    def test_error_no_address_with_extra_args(self):
        for response in self.env["iot.device"].parse_multi_input(
            self.device_identification, self.passphrase, [{"uuid": "abc"}]
        ):
            self.assertEqual(response["status"], "error")
            self.assertTrue("uuid" in response)

    def test_error_no_address(self):
        for response in self.env["iot.device"].parse_multi_input(
            self.device_identification, self.passphrase, [{"value": "test value"}]
        ):
            self.assertEqual(response["status"], "error")

    def test_correct_one_input(self):
        for response in self.env["iot.device"].parse_multi_input(
            self.device_identification,
            self.passphrase,
            [{"address": self.address_1, "value": "test"}],
        ):
            self.assertEqual(response["status"], "ok")

    def test_correct_two_inputs(self):
        for response in self.env["iot.device"].parse_multi_input(
            self.device_identification,
            self.passphrase,
            [
                {"address": self.address_1, "value": "test value 1"},
                {
                    "address": self.address_1,
                    "value": 2.3,
                },  # Checking that nothing wrong happens with a non string
                {"address": self.address_2, "value": "test value 3"},
            ],
        ):
            self.assertEqual(response["status"], "ok")

    def test_correct_with_extra_args(self):
        response_with_uuid = [
            {"address": self.address_1, "value": "test value 1", "uuid": "abc"},
            {"address": self.address_1, "value": "test value 2", "uuid": "def"},
            {"address": self.address_2, "value": "test value 3", "uuid": "ghi"},
        ]
        for response in self.env["iot.device"].parse_multi_input(
            self.device_identification, self.passphrase, response_with_uuid
        ):
            self.assertTrue(response["uuid"])
            self.assertEqual(
                response["message"],
                [x for x in response_with_uuid if x["uuid"] == response["uuid"]][0][
                    "value"
                ],
            )

    def test_error_archived_device(self):
        self.device.active = False
        self.assertEqual(
            self.env["iot.device"].parse_multi_input(
                self.device_identification,
                self.passphrase,
                [{"address": self.address_1, "value": "test"}],
            )["status"],
            "error",
        )

    def test_error_archived_device_input(self):
        self.device_input_1.active = False
        for result in self.env["iot.device"].parse_multi_input(
            self.device_identification,
            self.passphrase,
            [{"address": self.address_1, "value": "test"}],
        ):
            self.assertEqual(
                result["status"], "error",
            )

    def test_error_archived_device_input_extra_args(self):
        self.device_input_1.active = False
        for result in self.env["iot.device"].parse_multi_input(
            self.device_identification,
            self.passphrase,
            [{"address": self.address_1, "value": "test", "uuid": "ghi"}],
        ):
            self.assertEqual(
                result["status"], "error",
            )
            self.assertEqual(result["uuid"], "ghi")
