# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import uuid

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestEmployeeRfid(TransactionCase):
    def setUp(self):
        super(TestEmployeeRfid, self).setUp()
        self.employee = self.env["hr.employee"].create({"name": "Employee"})

    def test_generate(self):
        self.employee.write({"rfid_card_code": "1235"})
        self.assertFalse(self.employee.iot_key_id)
        self.employee.generate_iot_key()
        self.employee.refresh()
        self.assertTrue(self.employee.iot_key_id)
        self.assertEqual(
            self.employee.iot_key_id.unique_virtual_key,
            self.employee.rfid_card_code,
        )

        self.employee.write({"rfid_card_code": "125466"})
        self.assertEqual(
            self.employee.iot_key_id.unique_virtual_key,
            self.employee.rfid_card_code,
        )

    def test_unique_constrain(self):
        self.employee.write({"rfid_card_code": "1235"})
        self.employee.generate_iot_key()
        with self.assertRaises(ValidationError):
            self.env["iot.key"].create(
                {
                    "unique_virtual_key": uuid.uuid4(),
                    "res_model": self.employee._name,
                    "res_id": self.employee.id,
                }
            )
