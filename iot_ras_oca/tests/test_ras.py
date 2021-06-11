from odoo.tests.common import HttpCase


class TestRas(HttpCase):
    def setUp(self):
        super().setUp()
        self.card_code = "e313441e"
        self.employee = self.env["hr.employee"].create(
            {"name": "Anita", "rfid_card_code": self.card_code}
        )
        self.template = self.env.ref("iot_ras_oca.ras_template")

    def _get_wizard(self):
        wizard = self.env["iot.device.configure"].create({})
        self.assertFalse(wizard.serial)
        self.assertFalse(wizard.generated)
        self.assertFalse(wizard.url)
        wizard.run()
        self.assertTrue(wizard.serial)
        self.assertTrue(wizard.generated)
        self.assertTrue(wizard.url)
        return wizard

    def test_generation(self):
        wizard = self._get_wizard()
        device_config = self.url_open(
            wizard.url, data={"template": self.template.name}
        ).json()
        device = self.env["iot.device"].search([("name", "=", device_config["name"])])
        self.assertTrue(device)
        ras_input = device.input_ids
        self.assertTrue(ras_input)
        self.assertTrue(ras_input.serial)
        self.assertTrue(ras_input.passphrase)
        res = self.url_open(
            "/iot/%s/action" % ras_input.serial,
            data={"passphrase": ras_input.passphrase, "value": "123"},
        ).json()
        # This should work properly because it has not been assigned to
        # Checking attendance
        self.assertEqual(res["status"], "ok")

        ras_input.write(
            {
                "call_model_id": self.env.ref("hr.model_hr_employee").id,
                "call_function": "register_attendance",
            }
        )  # We are assigning it to the proper function and model

        res = self.url_open(
            "/iot/%s/action" % ras_input.serial,
            data={"passphrase": ras_input.passphrase, "value": "123"},
        ).json()
        # Now it must fail as the value is not correct
        self.assertEqual(res["status"], "ok")
        self.assertIn("error_message", res)
        self.assertRegex(res["error_message"], ".*No employee found.*")
        self.assertFalse(
            self.env["hr.attendance"].search([("employee_id", "=", self.employee.id)])
        )
        res = self.url_open(
            "/iot/%s/action" % ras_input.serial,
            data={"passphrase": ras_input.passphrase, "value": self.card_code},
        ).json()
        # The employee has checked in
        self.assertEqual(res["status"], "ok")
        self.assertEqual(res["action"], "check_in")
        self.assertEqual(res["error_message"], "")
        attendance = self.env["hr.attendance"].search(
            [("employee_id", "=", self.employee.id)]
        )
        self.assertTrue(attendance)
        self.assertEqual(1, len(attendance))
        self.assertFalse(attendance.check_out)
        res = self.url_open(
            "/iot/%s/action" % ras_input.serial,
            data={"passphrase": ras_input.passphrase, "value": self.card_code},
        ).json()
        # The employee has checked out
        self.assertEqual(res["status"], "ok")
        self.assertEqual(res["action"], "check_out")
        self.assertEqual(res["error_message"], "")
        attendance = self.env["hr.attendance"].search(
            [("employee_id", "=", self.employee.id)]
        )
        attendance.refresh()
        self.assertTrue(attendance)
        self.assertEqual(1, len(attendance))
        self.assertTrue(attendance.check_out)
