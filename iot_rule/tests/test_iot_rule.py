# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from mock import patch

from odoo.exceptions import ValidationError
from odoo.fields import Datetime
from odoo.tests.common import SavepointCase

from ..models.iot_key import IotKey


class TestIotRule(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestIotRule, cls).setUpClass()

        cls.rule_1 = cls.env["iot.rule"].create({"name": "rule 1"})
        cls.rule_2 = cls.env["iot.rule"].create({"name": "rule 2"})
        cls.lock_1 = cls.env["iot.lock"].create(
            {"name": "Lock 1", "rule_ids": [(4, cls.rule_1.id)]}
        )
        cls.type_of_key_1 = "RFID"
        cls.key_1 = cls.env["iot.key"].create(
            {
                "name": "Key 1",
                "rule_ids": [(4, cls.rule_1.id)],
                "key_type": cls.type_of_key_1,
            }
        )
        cls.type_of_key_2 = "UUID"
        cls.key_2 = cls.env["iot.key"].create(
            {
                "name": "Key 2",
                "rule_ids": [(4, cls.rule_2.id)],
                "key_type": cls.type_of_key_2,
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Demo partner"})
        cls.system = cls.env["iot.communication.system"].create({"name": "Testing"})
        cls.device_1 = cls.env["iot.device"].create(
            {"name": "device 1", "communication_system_id": cls.system.id}
        )
        cls.serial_of_input_1 = "serial 1"
        cls.passphrase_of_input_1 = "password 1"
        cls.name_of_input_1 = "name 1"
        cls.device_input_1 = cls.env["iot.device.input"].create(
            {
                "name": cls.name_of_input_1,
                "device_id": cls.device_1.id,
                "active": True,
                "serial": cls.serial_of_input_1,
                "passphrase": cls.passphrase_of_input_1,
                "call_model_id": cls.env.ref("iot_input_oca.model_iot_device_input").id,
                "call_function": "test_input_device",
                "lock_id": cls.lock_1.id,
            }
        )
        cls.device_2 = cls.env["iot.device"].create(
            {"name": "device 2", "communication_system_id": cls.system.id}
        )
        cls.serial_of_input_2 = "serial 2"
        cls.passphrase_of_input_2 = "password 2"
        cls.name_of_input_2 = "name 2"
        cls.device_input_2 = cls.env["iot.device.input"].create(
            {
                "name": cls.name_of_input_2,
                "device_id": cls.device_2.id,
                "active": True,
                "serial": cls.serial_of_input_2,
                "passphrase": cls.passphrase_of_input_2,
                "call_model_id": cls.env.ref("iot_input_oca.model_iot_device_input").id,
                "call_function": "test_input_device",
            }
        )
        cls.serial_of_input_without_device = "foo orphan"

    def test_allowed_access(self):
        self.assertTrue(
            self.lock_1.check_access_unique_virtual_key(self.key_1.unique_virtual_key)
        )

    def test_not_allowed_access(self):
        self.assertFalse(
            self.lock_1.check_access_unique_virtual_key(self.key_2.unique_virtual_key)
        )

    def test_non_existing_key(self):
        self.assertFalse(self.lock_1.action_ids)
        self.assertFalse(
            self.lock_1.check_access_unique_virtual_key(
                self.key_1.unique_virtual_key + self.key_2.unique_virtual_key
            )
        )
        self.assertTrue(self.lock_1.action_ids)
        self.assertFalse(self.lock_1.action_ids.key_id)

    def test_not_unique_key_model(self):
        self.key_1.write({"res_model": self.partner._name, "res_id": self.partner.id})

    def test_unique_key_models(self):
        with patch.object(IotKey, "_get_unique_key_models") as mocked:
            mocked.return_value = [self.partner._name]
            self.key_1.write(
                {"res_model": self.partner._name, "res_id": self.partner.id}
            )
            with self.assertRaises(ValidationError):
                self.key_2.write(
                    {"res_model": self.partner._name, "res_id": self.partner.id}
                )

    def test_inheritance(self):
        self.rule_1.parent_ids = [(4, self.rule_2.id)]
        self.assertTrue(
            self.lock_1.check_access_unique_virtual_key(self.key_2.unique_virtual_key)
        )

    def test_inheritance_loop(self):
        rule = self.env["iot.rule"].create({"name": "rule 1 0"})
        self.rule_1.parent_ids = [(4, rule.id)]
        for i in range(0, 50):
            key = self.env["iot.key"].create(
                {"name": "Key 2", "rule_ids": [(4, rule.id)]}
            )
            self.assertTrue(
                self.lock_1.check_access_unique_virtual_key(key.unique_virtual_key)
            )
            new_rule = self.env["iot.rule"].create({"name": "rule 1 %s" % i})
            rule.parent_ids = [(4, new_rule.id)]
            rule = new_rule
        key = self.env["iot.key"].create({"name": "Key 2", "rule_ids": [(4, rule.id)]})
        self.assertFalse(
            self.lock_1.check_access_unique_virtual_key(key.unique_virtual_key)
        )

    def test_recursion(self):
        self.rule_1.parent_ids = [(4, self.rule_2.id)]
        with self.assertRaises(ValidationError):
            self.rule_2.parent_ids = [(4, self.rule_1.id)]

    def test_actions(self):
        self.assertFalse(self.key_1.action_ids)
        self.assertFalse(self.lock_1.action_ids)
        self.lock_1.check_access_unique_virtual_key(self.key_1.unique_virtual_key)
        self.assertTrue(self.key_1.action_ids)
        self.assertTrue(self.lock_1.action_ids)
        self.assertFalse(self.key_2.action_ids)
        self.lock_1.check_access_unique_virtual_key(self.key_2.unique_virtual_key)
        self.assertTrue(self.key_2.action_ids)
        action = self.lock_1.view_actions()
        self.assertEqual(
            self.lock_1.action_ids,
            self.env[action["res_model"]].search(action["domain"]),
        )
        action = self.key_1.view_actions()
        self.assertEqual(
            self.env[action["res_model"]].search(action["domain"]),
            self.key_1.action_ids,
        )

    def test_expiration(self):
        self.assertTrue(
            self.lock_1.check_access_unique_virtual_key(self.key_1.unique_virtual_key)
        )
        now = Datetime.from_string(Datetime.now())
        self.key_1.expiration_date = Datetime.to_string(now + timedelta(hours=1))
        self.assertTrue(
            self.lock_1.check_access_unique_virtual_key(self.key_1.unique_virtual_key)
        )
        self.key_1.expiration_date = Datetime.to_string(now + timedelta(hours=-1))
        self.assertFalse(
            self.lock_1.check_access_unique_virtual_key(self.key_1.unique_virtual_key)
        )

    def test_lock_find_keys(self):
        result = self.lock_1.get_virtual_keys()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], self.key_1.id)
        key = self.env["iot.key"].create(
            {"name": "Key 1", "rule_ids": [(4, self.rule_1.id)]}
        )
        result = self.lock_1.get_virtual_keys()
        self.assertEqual(len(result), 2)
        ids = [r["id"] for r in result]
        self.assertIn(self.key_1.id, ids)
        self.assertIn(key.id, ids)
        now = Datetime.from_string(Datetime.now())
        key.expiration_date = Datetime.to_string(now + timedelta(hours=-1))
        result = self.lock_1.get_virtual_keys()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], self.key_1.id)
        key.expiration_date = Datetime.to_string(now + timedelta(hours=1))
        result = self.lock_1.get_virtual_keys()
        self.assertEqual(len(result), 2)
        ids = [r["id"] for r in result]
        self.assertIn(self.key_1.id, ids)
        self.assertIn(key.id, ids)

    def test_wizard(self):
        self.assertEqual(0, self.partner.iot_key_count)
        wizard_key = self.env["iot.key.wizard"].create(
            {
                "res_id": self.partner.id,
                "res_model": self.partner._name,
                "unique_virtual_key": "Testing Key",
                "rule_ids": [(4, self.rule_1.id)],
            }
        )
        wizard_key.create_key()
        key = wizard_key.iot_key_id
        self.assertEqual(key.unique_virtual_key, "Testing Key")
        self.assertEqual(key.rule_ids, self.rule_1)
        self.partner.refresh()
        self.assertEqual(1, self.partner.iot_key_count)
        action = self.partner.action_view_iot_key()
        self.assertEqual(key, self.env[action["res_model"]].search(action["domain"]))
        original_key = key
        wizard_key = self.env["iot.key.wizard"].create(
            {
                "res_id": self.partner.id,
                "res_model": self.partner._name,
                "iot_key_id": key.id,
                "unique_virtual_key": "Testing Key 2",
                "rule_ids": [(4, self.rule_1.id)],
            }
        )
        wizard_key.update_key()
        key.refresh()
        self.assertEqual(key.unique_virtual_key, "Testing Key 2")
        wizard_key = self.env["iot.key.wizard"].create(
            {
                "res_id": self.partner.id,
                "res_model": self.partner._name,
                "iot_key_id": key.id,
                "unique_virtual_key": "Testing Key",
                "rule_ids": [(4, self.rule_1.id)],
            }
        )
        wizard_key.create_key()
        key.refresh()
        self.assertEqual(key.unique_virtual_key, "Testing Key")
        self.assertEqual(key, original_key)

    def test_get_iot_keys_from_device_serial_and_type_of_key(self):
        result = self.env["iot.device"].get_iot_keys(
            self.serial_of_input_2, self.type_of_key_1
        )
        self.assertTrue(result.get("error", False))
        result = self.env["iot.device"].get_iot_keys(
            self.serial_of_input_without_device, self.type_of_key_1
        )
        self.assertTrue(result.get("error", False))
        result = self.env["iot.device"].get_iot_keys(
            self.serial_of_input_1, self.type_of_key_1
        )
        self.assertEqual(len(result["keys"]), 1)
        self.assertEqual(result["keys"][0].get("key_type"), self.type_of_key_1)
        result = self.env["iot.device"].get_iot_keys(
            self.serial_of_input_1, self.type_of_key_2
        )
        self.assertEqual(len(result["keys"]), 0)
        result = self.env["iot.device"].get_iot_keys(self.serial_of_input_1, "ALL")
        self.assertEqual(len(result["keys"]), 1)
        self.rule_1.write({"parent_ids": [(4, self.rule_2.id)]})
        result = self.env["iot.device"].get_iot_keys(self.serial_of_input_1, "ALL")
        self.assertEqual(len(result["keys"]), 2)

    def test_get_iot_keys_from_device_input(self):
        result = self.device_input_1.get_iot_keys()
        self.assertEqual(len(result["keys"]), 1)
        self.assertEqual(result["keys"][0].get("id"), self.key_1.id)

    def test_call_lock_of_a_device_input(self):
        self.assertTrue(
            self.device_input_1.call_lock(self.key_1.unique_virtual_key).get(
                "access_granted"
            )
        )

    def test_generate_iot_lock_for_device_input(self):
        self.device_2.write({"name": "Changing name"})
        self.assertFalse(self.device_input_2.lock_id)
        self.device_input_2.generate_iot_lock()
        lock = self.env["iot.lock"].search(
            [("id", "=", self.device_input_2.lock_id.id)], limit=1
        )
        self.assertEqual(
            lock.name, self.device_2.name + " / " + self.device_input_2.name
        )
        self.device_input_2.generate_iot_lock()
        self.assertEqual(lock, self.device_input_2.lock_id)

    def test_change_name_of_lock_if_device_name_changes(self):
        self.device_1_new_name = "some funky cool new name"
        self.device_1.write({"name": self.device_1_new_name})
        self.assertEqual(
            self.lock_1.name, self.device_1_new_name + " / " + self.device_input_1.name
        )
