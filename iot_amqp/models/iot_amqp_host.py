# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IotAmqpHost(models.Model):
    _name = 'iot.amqp.host'
    _description = 'Amqp Host'

    name = fields.Char(required=True)
    connection = fields.Char()
    active = fields.Boolean(default=True)
