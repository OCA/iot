# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class IotDeviceInput(models.Model):

    _inherit = "iot.device.input"

    def get_options(self):
        data = {}
        for option in self.device_id.option_ids:
            data[option.property_id.tech_name] = getattr(
                option, option.field_name, False
            )
            if (
                option.field_type == "bool"
                and option.property_id.is_action
                and option.value_bool
            ):
                option.value_bool = False
        return data
