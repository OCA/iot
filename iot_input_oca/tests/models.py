from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def test_fake_iot_input(self, value):
        partner = self.browse(value)
        partner.message_post(body=str(value))
        return {}
