# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IoTDeviceOutputAction(models.Model):
    _name = "iot.device.output.action"
    _description = "IoT Action"
    _order = "date_ok desc"

    output_id = fields.Many2one("iot.device.output", required=True, readonly=True)
    communication_system_action_id = fields.Many2one(
        "iot.communication.system.action", required=True
    )
    status = fields.Selection(
        [("ok", "Ok"), ("pending", "Pending"), ("failed", "Failed")],
        required=True,
        default="pending",
    )
    result = fields.Text()
    date_ok = fields.Datetime(readonly=True, string="Ok date")

    @api.constrains("output_id", "communication_system_action_id")
    def _check_system(self):
        if self.filtered(
            lambda r: r.output_id.communication_system_id
            != r.communication_system_action_id.communication_system_id
        ):
            raise ValidationError(_("Device and action must be of the same system"))

    def run_extra_actions(self, status, result):
        return

    def run(self):
        self.ensure_one()
        if self.status != "ok":
            status, result = self.communication_system_action_id.run(self)
            self.write(
                {
                    "status": status,
                    "result": result,
                    "date_ok": fields.Datetime.now() if status == "ok" else False,
                }
            )
            self.run_extra_actions(status, result)

    def autovacuum(self, **kwargs):
        """Delete data older than ``days``.
        Called from a cron.
        """
        deadline = datetime.now() - timedelta(**kwargs)
        records = self.search([("create_date", "<=", deadline)])
        nb_records = len(records)
        records.unlink()
        _logger.info("AUTOVACUUM - %s '%s' records deleted", nb_records, self._name)
        return True
