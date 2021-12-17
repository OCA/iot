# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from uuid import uuid4

from odoo import api, fields, models


class IotDeviceConfigure(models.TransientModel):
    _name = "iot.device.configure"
    _description = "Configure a IoT device"

    serial = fields.Char(readonly=True, required=True, default=lambda r: uuid4())
    url = fields.Char(compute="_compute_url")

    @api.depends("serial")
    def _compute_url(self):
        for record in self:
            record.url = (
                self.env["ir.config_parameter"].sudo().get_param("web.base.url")
                + "/iot/"
                + record.serial
                + "/configure"
            )

    @api.model
    def configure(self, serial, template_id, ip=False, **kwargs):
        config = self.search([("serial", "=", serial)])
        if not config:
            return {}
        config.unlink()
        device = self.env["iot.device"].create({"name": serial, "ip": ip})
        template = self.env["iot.template"].search([("name", "=", template_id)])
        if template:
            template.apply_template(device, template._get_keys(serial))
        return device.get_iot_configuration()
