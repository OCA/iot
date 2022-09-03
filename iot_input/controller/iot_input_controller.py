# Copyright 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
import logging
from odoo import http, _

_logger = logging.getLogger(__name__)


class CallIot(http.Controller):
    @http.route(
        ["/iot/<serial>/action"],
        type="http",
        auth="none",
        methods=["POST"],
        csrf=False,
    )
    def call_unauthorized_iot(self, serial, passphrase=None, *args, **kwargs):
        request = http.request
        if not request.env:
            return json.dumps(False)
        return json.dumps(
            request.env["iot.device.input"]
            .sudo()
            .get_device(serial, passphrase)
            .call_device(**kwargs)
        )

    @http.route(
        ["/iot/<device_identification>/multi_input"],
        type="http",
        auth="none",
        methods=["POST"],
        csrf=False,
    )
    def call_unauthorized_iot_multi_input(
        self, device_identification, passphrase=None, values=None, *args, **kwargs
    ):
        """Controller to write multiple input data to device inputs

        :param string passphrase:
            Device passphrase in POST data.

        :param string values:
            JSON formatted string containing a JSON an array of JSON objects.
        """
        request = http.request
        if not request.env:
            _logger.warning("env not set")
            return json.dumps({"status": "error", "message": _("Server Error")})
        if passphrase is None:
            _logger.warning("Passphrase is required")
            return json.dumps(
                {"status": "error", "message": _("Passphrase is required")}
            )
        if values is None:
            _logger.warning("Values is required")
            return json.dumps({"status": "error", "message": _("Values is required")})
        # Decode JSON object here and use pure python objects in further calls
        try:
            if isinstance(values, str):
                values = json.loads(values)
            if not isinstance(values, list):
                raise SyntaxError
        except json.decoder.JSONDecodeError:
            _logger.warning('Values is not a valid JSON')
            return json.dumps({'status': 'error',
                               'message': _('Values is not a valid JSON')})
        except SyntaxError:
            _logger.warning('Values should be a JSON array of JSON objects')
            return json.dumps({'status': 'error',
                               'message':
                               _('Values should be a JSON array of JSON objects')})
        # Encode response to JSON and return
        return json.dumps(
            request.env["iot.device"]
            .sudo()
            .parse_multi_input(device_identification, passphrase, values)
        )

    @http.route(
        ["/iot/<serial>/check"], type="http", auth="none", methods=["POST"], csrf=False
    )
    def check_unauthorized_iot(self, serial, *args, **kwargs):
        request = http.request
        if not request.env:
            return json.dumps(False)
        device = request.env['iot.device.input'].sudo().get_device(
            serial, kwargs['passphrase'])
        if device:
            return json.dumps({"state": True})
        return json.dumps({"state": False})
