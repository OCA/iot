# Copyright 2020 Dimitrios Tanis <dtanis@tanisfood.gr>
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2017 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime
import pytz
import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IotDeviceInput(models.Model):
    _inherit = "iot.device.input"

    action_type = fields.Selection(
        selection=[
            ("model", "Call model method"),
            ("event", "Log IoT event"),
        ],
        default="model",
        required=True,
        help="Type of action."
        "- Call model method: Use this to push data to another model's function"
        "- Log IoT event: Log data to the IoT event model",
    )
    default_value = fields.Char(
        help="Will be applied by default to all custom values of this "
             "event. This is a char field, so you have to enter some value "
             "that can be converted to the field type you choose.",
    )
    minimum = fields.Float(
        help="For numeric fields, it means the minimum possible value; "
             "for text fields, it means the minimum possible length. "
             "If it is bigger than the maximum, then this check is skipped",
    )
    maximum = fields.Float(
        default=-1,
        help="For numeric fields, it means the maximum possible value; "
             "for text fields, it means the maximum possible length. "
             "If it is smaller than the minimum, then this check is skipped",
    )
    field_type = fields.Selection(
        selection=[
            ("str", "Text"),
            ("int", "Whole number"),
            ("float", "Decimal number"),
            ("bool", "On/Off"),
        ],
        default="float",
        required=True,
        help="Type of information that can be stored in the event.",
    )
    alarm_type = fields.Selection(
        selection=[
            ("absolute", "Absolute Limits"),
            ("calculated", "Calculated"),
        ],
        default="absolute",
        required=True,
        help="Type of alarm.\n"
        "- Absolute: Alarm is fired when value is out of set limits\n"
        "- Calculated: Alarm is fired if c values in last n values are out of set limits\n",
    )
    limit_check = fields.Boolean(
        'Check Limits', help="Check if value is within limits")
    alarm_n = fields.Integer(
        'Count for Alarm', help="The number of values taken for the alarm calculation")
    alarm_c = fields.Integer(
        'Alarm Limit', help="The number of times the value is allowed to be out of"
        "limits before setting off the alarm")
    description = fields.Text('Description')
    notify_alarm = fields.Boolean(
        'Notify on Alarm', help="Send email when value is out of limits")
    user_ids = fields.Many2many('res.users', string='Users to notify',
                                help="Users to send email to when event is out of limits")

    event_ids = fields.One2many(
        comodel_name="iot.event",
        inverse_name="device_input_id",
        string="Events")
    event_count = fields.Integer(compute='_compute_event_count')

    @api.multi
    @api.depends('device_id')
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '[%s] %s' % (rec.device_id.name,
                                                rec.name)))
        return result

    def _check_default_value_one(self):
        if self.default_value:
            try:
                self.env["iot.event"]._transform_value(
                    self.default_value, self.field_type, self)
            except ValueError:
                selection = dict(
                    self._fields["field_type"].get_description(self.env)
                    ["selection"])
                raise ValidationError(
                    _("Default value %s cannot be converted to type %s.") %
                    (self.default_value, selection[self.field_type]))

    @api.constrains("default_value", "field_type")
    def _check_default_value(self):
        """Ensure the default value is valid."""
        for rec in self:
            rec._check_default_value_one()

    @api.multi
    @api.depends('event_ids')
    def _compute_event_count(self):
        for record in self:
            record.event_count = len(record.event_ids)

    @api.multi
    def action_show_events(self):
        self.ensure_one()
        action = self.env.ref('iot_event.iot_event_action')
        result = action.read()[0]

        result['context'] = {
            'default_device_input_id': self.id,
        }
        result['domain'] = "[('device_input_id', '=', " + \
                           str(self.id) + ")]"
        if len(self.event_ids) == 1:
            result['views'] = [(False, 'form')]
            result['res_id'] = self.event_ids.id
        return result

    @api.onchange('action_type')
    def _onchange_action_type(self):
        if self.action_type == 'event':
            self.call_model_id = False
            self.call_function = 'log_event'

    @api.model
    def log_event(self, value):
        '''Parse event data'''
        msg = {}
        res = {
            'value': value['value'],
        }

        def get_timestamp_utc(timestamp_input):
            if self.device_id.tz and self.device_id.tz not in ('GMT', 'UTC'):
                return fields.Datetime.to_string(
                    pytz.timezone(self.device_id.tz).localize(
                        fields.Datetime.from_string(timestamp_input),
                        is_dst=None).astimezone(pytz.utc))
            else:
                return timestamp_input

        if self.device_id.time_source == 'device':
            if 'timestamp' not in value.keys():
                _logger.warning('Missing timestamp key')
                msg = {'status': 'error',
                       'message': 'Error writing event data'}
                if 'uuid' in value.keys():
                    msg['uuid'] = value['uuid']
                return msg

            if isinstance(value['timestamp'], int):
                seconds_since_epoch = value['timestamp'] \
                    if value['timestamp'] > 1600000000 else value['timestamp'] * 1000
                t = fields.Datetime.to_string(datetime.datetime.fromtimestamp(seconds_since_epoch))
            else:
                t = value['timestamp']

            try:
                timestamp = get_timestamp_utc(t)
            except ValueError:
                _logger.warning('Wrong formatted Timestamp')
                msg = {'status': 'error',
                       'message': 'Wrong formatted Timestamp'}
                if 'uuid' in value.keys():
                    msg['uuid'] = value['uuid']
                return msg
            res['datetime_taken'] = timestamp,

        try:
            done = self.sudo().write({
                'event_ids': [(0, 0, res)]
            })
            if done:
                msg = {'status': 'ok'}
            else:
                _logger.warning('Error writing event data')
                msg = {'status': 'error',
                       'message': 'Error writing event data'}
        except ValueError:
            _logger.warning('ValueError in value')
            msg = {'status': 'error',
                   'message': 'ValueError in value'}

        if 'uuid' in value.keys():
            msg['uuid'] = value['uuid']
        return msg
