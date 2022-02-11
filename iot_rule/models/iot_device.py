# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class IotDevice(models.Model):
    _inherit = "iot.device"

    def get_iot_keys(self, serial_of_input, type_of_key):
        iot_input = self.env["iot.device.input"].search(
            [("serial", "=", serial_of_input)], limit=1
        )
        if iot_input:
            if iot_input.lock_id:
                result = iot_input.lock_id.get_virtual_keys()
                if type_of_key != "ALL":
                    result_filtered = []
                    for key in result:
                        if key["key_type"] == type_of_key:
                            result_filtered.append(key)
                    result = result_filtered
                return {"keys": result}
        return {"error": "no input found"}

    def write(self, vals):
        if vals.get("name", False):
            for device in self:
                for device_input in device.input_ids:
                    if device_input.lock_id:
                        input_name = device_input.name
                        device_input.lock_id.write(
                            {"name": vals.get("name") + " / " + input_name}
                        )
        return super(IotDevice, self).write(vals)
