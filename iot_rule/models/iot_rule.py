# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class IotRule(models.Model):

    _name = "iot.rule"
    _description = "IoT Rule (Relation Key-Lock)"

    name = fields.Char()
    active = fields.Boolean(default=True, required=True)
    lock_ids = fields.Many2many("iot.lock", string="Locks")
    parent_ids = fields.Many2many(
        "iot.rule",
        relation="iot_rule_implied_rel",
        column1="rule_id",
        column2="implied_rule_id",
    )

    def _check_access(self, key):
        if key.expiration_date and key.expiration_date < fields.Datetime.now():
            return False
        return self._check_access_recursion(key)

    def _check_access_recursion(self, key, limit=0):
        if not self:
            return False
        if limit > 50:
            return False
        if self & key.rule_ids:
            return True
        return self.mapped("parent_ids")._check_access_recursion(key, limit + 1)

    @api.constrains("parent_ids")
    def _check_recursion_parent_ids(self):
        if not self._check_m2m_recursion("parent_ids"):
            raise ValidationError(_("A recurssion was found"))

    def _get_virtual_keys(self, domain, limit=0):
        if not self or limit > 50:
            return self.env["iot.key"]
        return self.mapped("parent_ids")._get_virtual_keys(
            domain, limit + 1
        ) | self.env["iot.key"].search(
            domain
            + [
                ("rule_ids", "in", self.ids),
                "|",
                ("expiration_date", "=", False),
                ("expiration_date", ">=", fields.Datetime.now()),
            ]
        )
