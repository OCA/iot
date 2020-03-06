# Copyright 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
from odoo import http


class CallIot(http.Controller):
    @http.route([
        '/iot/<serial>/action',
        ], type='http', auth="none", methods=['POST'], csrf=False)
    def call_unauthorized_iot(self, serial, *args, **kwargs):
        request = http.request
        if not request.env:
            return json.dumps(False)
        return json.dumps(request.env['iot.device.input'].sudo().get_device(
            serial, kwargs['passphrase']).call_device(kwargs['value']))

    @http.route([
        '/iot/<serial>/check',
        ], type='http', auth="none", methods=['POST'], csrf=False)
    def check_unauthorized_iot(self, serial, *args, **kwargs):
        request = http.request
        if not request.env:
            return json.dumps(False)
        device = request.env['iot.device.input'].sudo().get_device(
            serial, kwargs['passphrase'])
        if device:
            return json.dumps({"state": True})
        return json.dumps({"state": False})
