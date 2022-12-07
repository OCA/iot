# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "IoT Key Employee RFID",
    "summary": """
        Use an Employee RFID Card as an IoT Key""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/iot",
    "depends": ["hr_attendance_rfid", "iot_rule"],
    "data": ["views/hr_employee.xml"],
}
