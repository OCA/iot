# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IotLock(models.Model):

    _name = "iot.lock"
    _description = "IoT Lock"

    name = fields.Char(required=True)
    description = fields.Text()
    rule_ids = fields.Many2many("iot.rule", string="Rules")
    action_ids = fields.One2many("iot.key.action", inverse_name="lock_id")
    active = fields.Boolean(default=True, required=True)

    def check_access_unique_virtual_key(self, unique_virtual_key):
        self.ensure_one()
        key = self.env["iot.key"].search(
            [("unique_virtual_key", "=", unique_virtual_key)], limit=1
        )
        if not key:
            self._missing_key(unique_virtual_key)
            return False
        return self.check_access(key)

    def _missing_key(self, unique_virtual_key):
        return self.env["iot.key.action"].create(
            self._missing_key_action_vals(unique_virtual_key)
        )

    def _missing_key_action_vals(self, unique_virtual_key):
        return {
            "lock_id": self.id,
            "unique_virtual_key": unique_virtual_key,
            "result": "refused",
        }

    def check_access(self, key):
        result = self.rule_ids._check_access(key)
        self.create_action(key, result)
        return result

    def create_action(self, key, result):
        return self.env["iot.key.action"].create(self._create_action_vals(key, result))

    def _create_action_vals(self, key, result):
        return {
            "lock_id": self.id,
            "key_id": key.id,
            "result": "accepted" if result else "refused",
        }

    def view_actions(self):
        self.ensure_one()
        action = self.env.ref("iot_rule.iot_key_action_act_window").read()[0]
        action["domain"] = [("lock_id", "=", self.id)]
        return action

    def get_virtual_keys(self, domain=None):
        self.ensure_one()
        if domain is None:
            domain = []
        keys = self.rule_ids._get_virtual_keys(domain)
        return keys.get_iot_rule_values()
