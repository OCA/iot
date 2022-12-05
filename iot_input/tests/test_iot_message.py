from odoo_test_helper import FakeModelLoader

from odoo.tests import SavepointCase


class TestIotInputMessage(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestIotInputMessage, cls).setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()

        from .models import ResPartner

        cls.loader.update_registry((ResPartner,))

        cls.partner = cls.env["res.partner"].create({"name": "IoT demo partner"})
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
                "call_model_id": cls.env.ref("base.model_res_partner").id,
                "call_function": "test_fake_iot_input",
            }
        )
        cls.iot = cls.env["iot.device.input"]

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super(TestIotInputMessage, cls).tearDownClass()

    def test_message(self):
        original_messages = self.partner.message_ids
        res = self.device_input.call_device(value=self.partner.id)
        self.assertEqual("ok", res["status"])
        new_message = self.partner.message_ids - original_messages
        self.assertTrue(new_message)
        self.assertEqual(1, len(new_message))
        self.assertRegex(new_message.body, ".*Detected automatically by.*")
