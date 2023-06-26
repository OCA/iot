# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IotDeviceInput(models.Model):
    _inherit = "iot.device.input"

    lock_id = fields.Many2one("iot.lock")

    def call_lock(self, value):
        result = self.lock_id.check_access_unique_virtual_key(value)
        return {"access_granted": result}

    def get_iot_keys(self, domain=None):
        if domain is None:
            domain = []
        return {"keys": self.lock_id.get_virtual_keys(domain)}

    def generate_iot_lock(self):
        self.ensure_one()
        if not self.lock_id:
            device_name = self.device_id.name
            lock = self.env["iot.lock"].create(
                {"name": device_name + " / " + self.name}
            )
            self.lock_id = lock.id
        return {}
