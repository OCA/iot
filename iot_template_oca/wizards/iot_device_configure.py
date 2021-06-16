# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from uuid import uuid4

from odoo import _, api, fields, models


class IotDeviceConfigure(models.TransientModel):
    _name = "iot.device.configure"
    _description = "Configure a IoT device"

    generated = fields.Boolean(default=False)
    serial = fields.Char(readonly=True)
    url = fields.Char(compute="_compute_url")

    @api.depends("serial")
    def _compute_url(self):
        for record in self:
            url = False
            if record.generated:
                url = (
                    self.env["ir.config_parameter"].sudo().get_param("web.base.url")
                    + "/iot/"
                    + record.serial
                    + "/configure"
                )
            record.url = url

    def run(self):
        if not self.generated:
            self.write({"generated": True, "serial": uuid4()})
        return {
            "name": _("Configure device"),
            "type": "ir.actions.act_window",
            "res_model": "iot.device.configure",
            "view_mode": "form",
            "target": "new",
            "res_id": self.id,
            "context": self.env.context,
        }

    @api.model
    def configure(self, serial, template_id):
        config = self.search([("serial", "=", serial)])
        if not config:
            return {}
        config.unlink()
        device = self.env["iot.device"].create({"name": serial})
        template = self.env["iot.template"].search([("name", "=", template_id)])
        if template:
            template.apply_template(device, template._get_keys(serial))
        return device.get_iot_configuration()
