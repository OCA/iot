from odoo import models
from uuid import uuid4


class IotTemplate(models.Model):
    _inherit = 'iot.template'

    def auto_generate_key(self, serial):
        res = super().auto_generate_key(serial)
        if self == self.env.ref('iot_ras.ras_template'):
            res.update({
                'key_serial': uuid4(),
                'passphrase': uuid4(),
            })
        return res
