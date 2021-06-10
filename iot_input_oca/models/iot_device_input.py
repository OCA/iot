from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class IotDeviceInput(models.Model):
    _name = "iot.device.input"
    _description = "Device input"
    _order = "name"

    name = fields.Char(required=True)
    device_id = fields.Many2one("iot.device", required=True, readonly=True)
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

    @api.depends("action_ids")
    def _compute_action_count(self):
        for r in self:
            r.action_count = len(r.action_ids)

    def _call_device(self, value):
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
        return getattr(obj, self.call_function)(value)

    def parse_args(self, serial, passphrase):
        if not serial or not passphrase:
            raise ValidationError(_("Serial and passphrase are required"))
        return [("serial", "=", serial), ("passphrase", "=", passphrase)]

    @api.model
    def get_device(self, serial, passphrase):
        return self.search(self.parse_args(serial, passphrase), limit=1)

    def call_device(self, value):
        if not self:
            return {"status": "error", "message": _("Device cannot be found")}
        else:
            res = self._call_device(value)
            res["status"] = "ok"
        self.env["iot.device.input.action"].create(self._add_action_vals(value, res))
        return res

    def _add_action_vals(self, value, res):
        return {
            "input_id": self.id,
            "args": str(value),
            "res": str(res),
        }

    def test_input_device(self, value):
        return {"value": value}

    def test_model_function(self, value):
        return {"status": "ok", "message": value}


class IoTDeviceAction(models.Model):
    _name = "iot.device.input.action"
    _description = "Action of device inputs"

    input_id = fields.Many2one("iot.device.input")
    args = fields.Char()
    res = fields.Char()
