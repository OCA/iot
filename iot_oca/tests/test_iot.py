# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unittest.mock import patch

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestIoT(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.system = cls.env["iot.communication.system"].create({"name": "Testing"})
        cls.system_2 = cls.env["iot.communication.system"].create(
            {"name": "Testing 02"}
        )
        cls.action = cls.env["iot.communication.system.action"].create(
            {"name": "test", "communication_system_id": cls.system.id}
        )
        cls.action_2 = cls.env["iot.communication.system.action"].create(
            {"name": "test 02", "communication_system_id": cls.system_2.id}
        )
        cls.device = cls.env["iot.device"].create(
            {"name": "Device", "communication_system_id": cls.system.id}
        )

    def test_action(self):
        self.assertEqual(self.device.action_count, 0)
        with mute_logger("odoo.addons.iot_oca.models.iot_communication_system_action"):
            self.device.with_context(
                iot_communication_system_action_id=self.action.id
            ).device_run_action()
        self.assertEqual(self.device.action_count, 1)
        self.assertEqual(self.device.action_ids.status, "failed")

    def test_correct_action(self):
        self.assertEqual(self.device.action_count, 0)
        with patch(
            "odoo.addons.iot_oca.models.iot_communication_system_action."
            "IoTSystemAction._run",
            return_value=("ok", ""),
        ):
            self.device.with_context(
                iot_communication_system_action_id=self.action.id
            ).device_run_action()
        self.assertEqual(self.device.action_count, 1)
        self.assertEqual(self.device.action_ids.status, "ok")

    def test_constrains(self):
        with self.assertRaises(ValidationError):
            self.device.with_context(
                iot_communication_system_action_id=self.action_2.id
            ).device_run_action()

    def test_rerun_failed_action(self):
        with mute_logger("odoo.addons.iot_oca.models.iot_communication_system_action"):
            self.device.with_context(
                iot_communication_system_action_id=self.action.id
            ).device_run_action()
        device_action = self.device.action_ids
        self.assertEqual(device_action.status, "failed")
        self.assertFalse(device_action.date_ok)
        with patch(
            "odoo.addons.iot_oca.models.iot_communication_system_action."
            "IoTSystemAction._run",
            return_value="done",
        ):
            device_action.run()
        self.assertEqual(device_action.status, "ok")
        self.assertEqual(device_action.result, "done")
        self.assertTrue(device_action.date_ok)
