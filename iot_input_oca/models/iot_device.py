import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class IotDevice(models.Model):
    _inherit = "iot.device"

    input_ids = fields.One2many("iot.device.input", inverse_name="device_id")
    input_count = fields.Integer(compute="_compute_input_count")

    @api.depends("input_ids")
    def _compute_input_count(self):
        for r in self:
            r.input_count = len(r.input_ids)

    def action_show_input(self):
        self.ensure_one()
        action = self.env.ref("iot_input_oca.iot_device_input_action")
        result = action.read()[0]

        result["context"] = {
            "default_device_id": self.id,
        }
        result["domain"] = [("device_id", "=", self.id)]
        if len(self.input_ids) == 1:
            result["views"] = [(False, "form")]
            result["res_id"] = self.input_ids.id
        return result

    def parse_single_input(self, uuid=False, address=False, **kwargs):
        """Handle single input for device

        :param dict value:
            Dict containing at least keys 'address', 'value'
        :returns: dict with keys 'status', 'message' where:
            - status='ok' when value is parsed without errors
            - status='error' and message='error message' when error occurs
            If value contains a value with key 'uuid', it is passed in the return dict
            to identify result for each entry at the iot end
        :rtype: dict
        """
        msg = {}
        if uuid:
            msg["uuid"] = uuid
        if not address:
            _logger.warning("Address for Input is required")
            msg.update(
                {"status": "error", "message": _("Address for Input is required")}
            )
            return msg
        device_input = self.input_ids.filtered(lambda i: i.address == str(address))
        if len(device_input) == 1:
            if not device_input.active:
                _logger.warning(
                    "Input with address %s is inactive, no data will be logged",
                    device_input.address,
                )
                msg.update(
                    {
                        "status": "error",
                        "message": _("Server Error. Check server logs"),
                    }
                )
                return msg
            res = device_input.call_device(**kwargs)
            if uuid:
                res["uuid"] = uuid
            return res
        else:
            _logger.warning("Input with address %s not found", address)
            msg.update(
                {"status": "error", "message": _("Server Error. Check server logs")}
            )
            return msg
