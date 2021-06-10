from uuid import uuid4

from odoo import models


class IotTemplate(models.Model):
    _inherit = "iot.template"

    def auto_generate_key(self, serial):
        res = super().auto_generate_key(serial)
        if self == self.env.ref("iot_ras_oca.ras_template"):
            res.update({"key_serial": uuid4(), "passphrase": uuid4()})
        return res
