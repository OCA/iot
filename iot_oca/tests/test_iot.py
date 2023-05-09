# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from mock import patch

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestIoT(TransactionCase):
    def setUp(self):
        super().setUp()
        self.system = self.env["iot.communication.system"].create({"name": "Testing"})
        self.system_2 = self.env["iot.communication.system"].create(
            {"name": "Testing 02"}
        )
        self.action = self.env["iot.communication.system.action"].create(
            {"name": "test", "communication_system_id": self.system.id}
        )
        self.action_2 = self.env["iot.communication.system.action"].create(
            {"name": "test 02", "communication_system_id": self.system_2.id}
        )
        self.device = self.env["iot.device"].create(
            {"name": "Device", "communication_system_id": self.system.id}
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
