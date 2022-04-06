import logging
import traceback
from io import StringIO

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class IotDeviceInput(models.Model):
    _name = "iot.device.input"
    _description = "Device input"
    _order = "name"

    name = fields.Char(required=True)
    device_id = fields.Many2one(
        "iot.device", required=True, readonly=True, auto_join=True, ondelete="cascade"
    )
    call_model_id = fields.Many2one("ir.model")
    call_function = fields.Char(required=True)
    active = fields.Boolean(default=True)
    serial = fields.Char()
    address = fields.Char()
    passphrase = fields.Char()
    action_ids = fields.One2many(
        "iot.device.input.action", inverse_name="input_id", readonly=True,
    )
    action_count = fields.Integer(compute="_compute_action_count")
    lang = fields.Selection(
        selection=lambda self: self.env["res.lang"].get_installed(), string="Language",
    )
    verbose_logging = fields.Boolean()

    @api.depends("action_ids")
    def _compute_action_count(self):
        for r in self:
            r.action_count = len(r.action_ids)

    def _call_device(self, *args, **kwargs):
        self.ensure_one()
        obj = self
        if self.call_model_id:
            obj = self.env[self.call_model_id.model].with_context(
                iot_device_input_id=self.id,
                iot_device_name=self.device_id.name,
                iot_device_id=self.device_id.id,
            )
        if self.lang:
            obj = obj.with_context(lang=self.lang)
        return getattr(obj, self.call_function)(*args, **kwargs)

    def parse_args(self, serial, passphrase):
        if not serial or not passphrase:
            raise ValidationError(_("Serial and passphrase are required"))
        return [
            ("serial", "=", serial),
            ("passphrase", "=", passphrase),
            ("device_id.active", "=", True),
        ]

    @api.model
    def get_device(self, serial, passphrase):
        return self.search(self.parse_args(serial, passphrase), limit=1)

    def call_device(self, **kwargs):
        if not self:
            return {"status": "error", "message": _("Device cannot be found")}
        new_kwargs = kwargs.copy()
        args = []
        if "value" in new_kwargs and len(new_kwargs) == 1:
            args.append(new_kwargs.pop("value"))
        try:
            # We want to control that if an error happens,
            # everything will return to normal but we can process it properly
            with self.env.cr.savepoint():
                res = self._call_device(*args, **new_kwargs)
                res["status"] = "ok"
                error = False
        except self._swallable_exceptions():
            buff = StringIO()
            traceback.print_exc(file=buff)
            error = buff.getvalue()
            _logger.error(error)
            res = {"status": "ko"}
        self.device_id.last_contact_date = fields.Datetime.now()
        self._add_log(res, error, args, new_kwargs)
        return res

    def _add_log(self, res, error, args, new_kwargs):
        if not self.verbose_logging:
            return
        self.env["iot.device.input.action"].create(
            self._add_action_vals(res, error, args, new_kwargs)
        )

    def _swallable_exceptions(self):
        # TODO: improve this list
        return (UserError, ValidationError, AttributeError, TypeError)

    def _add_action_vals(self, res, error, args, kwargs):
        new_res = res.copy()
        if error:
            new_res["error"] = error
        return {
            "input_id": self.id,
            "args": str(args or kwargs),
            "res": str(res),
        }

    def test_input_device(self, value):
        return {"value": value}

    def test_model_function(self, value):
        return {"status": "ok", "message": value}

    def show_actions(self):
        self.ensure_one()
        action = self.env.ref("iot_input_oca.iot_device_input_action_action").read()[0]
        action["domain"] = [("input_id", "=", self.id)]
        return action


class IoTDeviceAction(models.Model):
    _name = "iot.device.input.action"
    _description = "Action of device inputs"

    input_id = fields.Many2one("iot.device.input", ondelete="cascade")
    args = fields.Char()
    kwargs = fields.Char()
    res = fields.Char()
