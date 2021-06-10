# Copyright 2017 Comunitea Servicios Tecnológicos S.L.
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import logging

from odoo import _, api, models

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def register_attendance(self, card_code):
        res = super().register_attendance(card_code)
        if "action" in res:
            if res["action"] == "check_in":
                res["action_msg"] = _("Checked in %s") % res["employee_name"]
            elif res["action"] == "check_out":
                res["action_msg"] = _("Checked out %s") % res["employee_name"]
            elif res["action"] == "FALSE":
                res["action_msg"] = _("Contact your admin")
        return res
