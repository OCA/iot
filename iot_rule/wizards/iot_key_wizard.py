# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class OddoorKeyWizard(models.TransientModel):

    _name = "iot.key.wizard"
    _description = "Create a Key"

    res_id = fields.Integer(required=True)
    res_model = fields.Char(required=True)
    iot_key_id = fields.Many2one(
        "iot.key",
    )
    unique_virtual_key = fields.Char(required=True)
    rule_ids = fields.Many2many("iot.rule")

    def _create_iot_key_vals(self):
        record = self.env[self.res_model].browse(self.res_id)
        return {
            "res_id": self.res_id,
            "res_model": self.res_model,
            "name": _("Key of %s") % record.display_name,
            "unique_virtual_key": self.unique_virtual_key,
            "rule_ids": [(6, 0, self.rule_ids.ids)],
        }

    def create_key(self):
        self.ensure_one()
        if not self.iot_key_id:
            self.iot_key_id = self.env["iot.key"].create(self._create_iot_key_vals())
            return self.update_key(False)
        return self.update_key()

    def _update_key_vals(self):
        record = self.env[self.res_model].browse(self.res_id)
        return {
            "unique_virtual_key": self.unique_virtual_key,
            "name": _("Key of %s") % record.display_name,
            "rule_ids": [(6, 0, self.rule_ids.ids)],
        }

    def update_key(self, update=True):
        if update:
            self.iot_key_id.write(self._update_key_vals())
        return {}
