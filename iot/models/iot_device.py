# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, tools


class IoTDevice(models.Model):
    _name = "iot.device"
    _description = "IoT Device"
    image = fields.Binary(
        attachment=True,
        help="This field holds the image used as image for the equipment, "
             "limited to 1024x1024px.",
    )
    image_medium = fields.Binary(
        string="Medium-sized image",
        attachment=True,
        help="Medium-sized image of the equipment. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved, "
             "only when the image exceeds one of those sizes. Use this "
             "field in form views or some kanban views.")
    image_small = fields.Binary(
        string="Small-sized image",
        attachment=True,
        help="Small-sized image of the equipment. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.",
    )

    name = fields.Char(required=True)
    system_id = fields.Many2one('iot.system', required=True)
    action_ids = fields.One2many(
        'iot.device.action',
        inverse_name='device_id'
    )
    active = fields.Boolean(default=True)
    device_identification = fields.Char()
    passphrase = fields.Char()
    # TODO: On 14 remove passpharse and device_identification.
    #  Create a multiparameter input in order to manage this
    state = fields.Selection([], readonly=True)
    model = fields.Char()
    ip = fields.Char(string="IP")
    action_count = fields.Integer(compute='_compute_action_count')
    group_id = fields.Many2one("iot.device.group")
    tag_ids = fields.Many2many("iot.device.tag")
    color = fields.Integer()
    last_contact_date = fields.Datetime(readonly=True)
    icon = fields.Selection(
        [
            ("fa fa-television fa-4x", "television"),
            ("fa fa-wifi fa-4x", "wifi"),
            ("fa fa-laptop fa-4x", "laptop"),
            ("fa fa-desktop fa-4x", "desktop"),
            ("fa fa-archive fa-4x", "archive"),
            ("fa fa-mobile fa-6x", "mobile"),
        ],
        "Icon",
    )

    @api.multi
    @api.depends('action_ids')
    def _compute_action_count(self):
        for record in self:
            record.action_count = len(record.action_ids)

    @api.multi
    def device_run_action(self):
        system_action = self.env['iot.system.action'].browse(
            self.env.context.get('iot_system_action_id'))
        for rec in self:
            action = self.env['iot.device.action'].create({
                'device_id': rec.id,
                'system_action_id': system_action.id,
            })
            action.run()

    @api.model_create_multi
    def create(self, values):
        for vals in values:
            tools.image_resize_images(vals, sizes={'image': (1024, None)})
        return super().create(values)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals, sizes={'image': (1024, None)})
        return super().write(vals)
