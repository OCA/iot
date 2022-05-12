# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json

from odoo import http


class CallIot(http.Controller):
    @http.route(
        ["/iot/<serial>/configure"],
        type="http",
        auth="none",
        methods=["POST"],
        csrf=False,
    )
    def configure_iot(self, serial, template, **kwargs):
        request = http.request
        if not request.env:
            return json.dumps(False)
        return json.dumps(
            request.env["iot.device.configure"]
            .sudo()
            .configure(serial, template, **kwargs)
        )
