from odoo.tests.common import SavepointCase
from odoo.tools import mute_logger


class TestIotIn(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.device_identification = "test_device_name"
        cls.passphrase = "password"

        cls.system = cls.env["iot.communication.system"].create({"name": "Demo system"})
        cls.device = cls.env["iot.device"].create(
            {
                "name": "Device",
                "communication_system_id": cls.system.id,
            }
        )
        cls.address_1 = "I0"
        cls.device_input_1 = cls.env["iot.device.input"].create(
            {
                "name": "Input 1",
                "device_id": cls.device.id,
                "address": cls.address_1,
                "call_model_id": cls.env.ref("iot_input_oca.model_iot_device_input").id,
                "call_function": "test_model_function",
            }
        )
        cls.address_2 = "I1"
        cls.env["iot.device.input"].create(
            {
                "name": "Input 2",
                "device_id": cls.device.id,
                "address": cls.address_2,
                "call_model_id": cls.env.ref("iot_input_oca.model_iot_device_input").id,
                "call_function": "test_model_function",
            }
        )
        cls.env["iot.device.input"].create(
            {
                "name": "Multi Input",
                "device_id": cls.device.id,
                "serial": cls.device_identification,
                "passphrase": cls.passphrase,
                "call_function": "parse_multi_input",
            }
        )
        cls.single_input_values = [{"input": cls.address_1, "value": "test"}]
        cls.iot = cls.env["iot.device.input"]

    def remove_test_multi_input_error_wrong_identification(self):
        iot = self.iot.get_device(
            serial=self.device_identification + self.device_identification,
            passphrase=self.passphrase,
        )
        self.assertEqual(
            iot.call_device(values=self.single_input_values)["status"],
            "ko",
        )

    def test_multi_input_error_no_inputs(self):
        iot = self.iot.get_device(
            serial=self.device_identification, passphrase=self.passphrase
        )
        self.assertEqual(
            iot.call_device(values=[])["status"],
            "ko",
        )

    def test_multi_input_non_existing_address(self):
        non_existing_address = "I3"
        iot = self.iot.get_device(
            serial=self.device_identification, passphrase=self.passphrase
        )
        for response in iot.call_device(
            values=[{"address": non_existing_address, "value": "test value 1"}],
        )["result"]:
            self.assertEqual(response["status"], "error")

    @mute_logger("odoo.addons.iot_input_oca.models.iot_device_input")
    def test_error_missing_parameter(self):
        iot = self.iot.get_device(
            serial=self.device_identification, passphrase=self.passphrase
        )
        for response in iot.call_device(values=[{"address": self.address_1}])["result"]:
            self.assertEqual(response["status"], "ko")

    @mute_logger("odoo.addons.iot_input_oca.models.iot_device_input")
    def test_error_with_extra_args(self):

        iot = self.iot.get_device(
            serial=self.device_identification, passphrase=self.passphrase
        )
        for response in iot.call_device(
            values=[{"address": self.address_1, "uuid": "abc"}],
        )["result"]:
            self.assertEqual(response["status"], "ko")
            self.assertTrue("uuid" in response)

    def test_error_no_address_with_extra_args(self):
        iot = self.iot.get_device(
            serial=self.device_identification, passphrase=self.passphrase
        )
        for response in iot.call_device(values=[{"uuid": "abc"}])["result"]:
            self.assertEqual(response["status"], "error")
            self.assertTrue("uuid" in response)

    def test_error_no_address(self):
        iot = self.iot.get_device(
            serial=self.device_identification, passphrase=self.passphrase
        )
        for response in iot.call_device(values=[{"value": "test value"}])["result"]:
            self.assertEqual(response["status"], "error")

    def test_correct_one_input(self):
        iot = self.iot.get_device(
            serial=self.device_identification, passphrase=self.passphrase
        )
        for response in iot.call_device(
            values=[{"address": self.address_1, "value": "test"}],
        )["result"]:
            self.assertEqual(response["status"], "ok")

    def test_correct_two_inputs(self):
        iot = self.iot.get_device(
            serial=self.device_identification, passphrase=self.passphrase
        )
        for response in iot.call_device(
            values=[
                {"address": self.address_1, "value": "test value 1"},
                {
                    "address": self.address_1,
                    "value": 2.3,
                },  # Checking that nothing wrong happens with a non string
                {"address": self.address_2, "value": "test value 3"},
            ],
        )["result"]:
            self.assertEqual(response["status"], "ok")

    def test_correct_with_extra_args(self):
        iot = self.iot.get_device(
            serial=self.device_identification, passphrase=self.passphrase
        )
        response_with_uuid = [
            {"address": self.address_1, "value": "test value 1", "uuid": "abc"},
            {"address": self.address_1, "value": "test value 2", "uuid": "def"},
            {"address": self.address_2, "value": "test value 3", "uuid": "ghi"},
        ]
        for response in iot.call_device(values=response_with_uuid)["result"]:
            self.assertTrue(response["uuid"])
            self.assertEqual(
                response["message"],
                [x for x in response_with_uuid if x["uuid"] == response["uuid"]][0][
                    "value"
                ],
            )

    def test_error_archived_device(self):
        self.device.active = False
        iot = self.iot.get_device(
            serial=self.device_identification, passphrase=self.passphrase
        )
        self.assertEqual(
            iot.call_device(
                values=[{"address": self.address_1, "value": "test"}],
            )["status"],
            "error",
        )

    def test_error_archived_device_input(self):
        self.device_input_1.active = False
        iot = self.iot.get_device(
            serial=self.device_identification, passphrase=self.passphrase
        )
        for result in iot.call_device(
            values=[{"address": self.address_1, "value": "test"}],
        )["result"]:
            self.assertEqual(
                result["status"],
                "error",
            )

    def test_error_archived_device_input_extra_args(self):
        self.device_input_1.active = False
        iot = self.iot.get_device(
            serial=self.device_identification, passphrase=self.passphrase
        )
        for result in iot.call_device(
            values=[{"address": self.address_1, "value": "test", "uuid": "ghi"}],
        )["result"]:
            self.assertEqual(
                result["status"],
                "error",
            )
            self.assertEqual(result["uuid"], "ghi")
