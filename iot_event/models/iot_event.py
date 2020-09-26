# Copyright 2020 Dimitrios Tanis <dtanis@tanisfood.gr>
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2017 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.tools import float_compare


BOOL_OFF_VALUES = [
    "0", "false", "", "no", "off", "offline", _("No").lower()
]


class IotEvents(models.Model):
    _name = "iot.event"
    _description = 'Iot Events'
    _order = 'datetime_taken DESC, device_id, device_input_id'

    @api.multi
    def _limit_exceeded(self):
        """compute the value of the function field"""
        precision = self.env['decimal.precision'].precision_get(
            'IoT Event Value Presision')
        for record in self:
            if record.field_type == 'int':
                record.out_of_min_limit = record.value_int <= record.minimum
                record.out_of_max_limit = record.value_int >= record.maximum
            if record.field_type == 'float':
                record.out_of_min_limit = float_compare(
                    record.value_float, record.minimum, precision_digits=precision) == -1
                record.out_of_max_limit = float_compare(
                    record.value_float, record.maximum, precision_digits=precision) == 1
            elif record.field_type == 'str':
                record.out_of_min_limit = len(self.value_str) <= record.minimum
                record.out_of_max_limit = len(self.value_str) >= record.maximum

    def _build_search(self, operator, limit):
        match_ids = []
        query = "SELECT l.id FROM iot_event l " \
                'INNER JOIN iot_device_input i ON l.device_input_id = i.id ' \
                "WHERE i.minimum < i.maximum AND " \
                "CASE WHEN i.field_type = 'int' THEN l.value_int " \
                "WHEN  i.field_type = 'float' THEN l.value_float END " \
                "{op} i.{limit}".format(op=operator, limit=limit)
        self.env.cr.execute(query)
        for row in self.env.cr.fetchall():
            match_ids.append(row[0])
        if match_ids:
            # return domain matching the selected ids
            return [('id', 'in', match_ids)]
        else:
            # return a domain which will never yield a result
            return [('id', '=', 0)]

    def _search_min_limit_exceeded(self, operator, value):
        return self._build_search('<', 'minimum')

    def _search_max_limit_exceeded(self, operator, value):
        return self._build_search('>', 'maximum')

    @api.multi
    @api.depends('datetime_taken')
    def _compute_time(self):
        for rec in self:
            current_datetime = fields.Datetime.context_timestamp(
                rec, fields.Datetime.from_string(rec.datetime_taken))
            rec.datetaken = current_datetime.date()
            rec.timetaken = current_datetime.hour + current_datetime.minute / 60.0

    device_input_id = fields.Many2one('iot.device.input', required=True)
    device_id = fields.Many2one(related="device_input_id.device_id")
    field_name = fields.Char(
        compute="_compute_field_name",
        help="Technical name of the field where the value is stored.",
    )
    field_type = fields.Selection(
        related="device_input_id.field_type", readonly=True,
    )
    minimum = fields.Float(related='device_input_id.minimum')
    maximum = fields.Float(related='device_input_id.maximum')
    out_of_min_limit = fields.Boolean(
        compute=_limit_exceeded,
        search=_search_min_limit_exceeded,
        string='Event logged out of Minimum limit')
    out_of_max_limit = fields.Boolean(
        compute=_limit_exceeded,
        search=_search_max_limit_exceeded,
        string='Event logged out of Maximum limit')

    datetime_taken = fields.Datetime('Datetime Taken',
                                     default=lambda self: fields.datetime.now())
    datetaken = fields.Date('Date Taken', index=True,
                            compute="_compute_time", store=True,
                            help="Date on which the Temp was taken.")
    timetaken = fields.Float('Time Taken', index=True,
                             compute="_compute_time", store=True,
                             help="Time on which the Temp was taken.")
    value = fields.Char(
        compute="_compute_value", inverse="_inverse_value",
        search="_search_value",
        help="Value, always converted to/from the typed field.",
    )
    value_str = fields.Char(string="Text value", index=True)
    value_int = fields.Integer(string="Whole number value", index=True)
    value_float = fields.Float(string="Decimal number value", index=True)
    value_bool = fields.Integer(string="On/Off value", index=True)

    @api.multi
    @api.depends("device_input_id.field_type")
    def _compute_field_name(self):
        """Get the technical name where the real typed value is stored."""
        for s in self:
            s.field_name = "value_{!s}".format(s.device_input_id.field_type)

    @api.multi
    @api.depends("device_input_id.field_type", "field_name", "value_str",
                 "value_int", "value_float", "value_bool")
    def _compute_value(self):
        """Get the value as a string, from the original field."""
        for s in self:
            if s.field_type == "bool":
                s.value = _("False") if s.value_bool == 0 else _("True")
            else:
                s.value = getattr(s, s.field_name, False)

    @api.multi
    def _inverse_value(self):
        """Write the value correctly converted in the typed field."""
        for record in self:
            record[record.field_name] = self._transform_value(
                record.value, record.field_type
            )

    @api.onchange('value')
    def _onchange_value(self):
        """Inverse function is not launched after writing, so we need to
        trigger it right now."""
        self._inverse_value()

    @api.model
    def _transform_value(self, value, format_):
        """Transforms a text value to the expected format.

        :param str/bool value:
            Custom value in raw string.

        :param str format_:
            Target conversion format for the value. Must be available among
            ``custom.info.property`` options.
        """
        if not value:
            value = False
        elif format_ == "bool":
            value = value.strip().lower() not in BOOL_OFF_VALUES
        elif format_ != "str":
            value = safe_eval("{!s}({!r})".format(format_, value))
        return value

    @api.model
    def _search_value(self, operator, value):
        """Search from the stored field directly."""
        options = (
            o[0] for o in
            self.device_input_id._fields["field_type"]
            .get_description(self.env)["selection"])
        domain = []
        for fmt in options:
            try:
                _value = (self._transform_value(value, fmt)
                          if not isinstance(value, list) else
                          [self._transform_value(v, fmt) for v in value])
            except ValueError:
                # If you are searching something that cannot be casted, then
                # your property is probably from another type
                continue
            domain += [
                "&",
                ("field_type", "=", fmt),
                ("value_" + fmt, operator, _value),
            ]
        return ["|"] * int(len(domain) / 3 - 1) + domain

    @api.multi
    @api.depends('device_input_id')
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s:%s' % (rec.device_id.name,
                                              rec.device_input_id.name)))
        return result

    @api.multi
    def send_alarm_mail(self):
        mail_template = self.env.ref(
            'iot_event.iot_event_alarm_email_template')
        for rec in self:
            mail_template.send_mail(
                rec.id, force_send=True, raise_exception=True)

    @api.model
    def create(self, vals_list):
        res = super(IotEvents, self).create(vals_list)
        if res.device_input_id.notify_alarm:
            if res.device_input_id.alarm_type == 'absolute':
                if res.out_of_min_limit or res.out_of_max_limit:
                    res.send_alarm_mail()
            elif res.device_input_id.alarm_type == 'calculated':
                alarms = res.test_alarm()
                if alarms:
                    res.with_context(alarms=alarms).send_alarm_mail()
        return res

    @api.multi
    def test_alarm(self):
        items = []
        for rec in self:
            events = self.search(
                [('device_input_id', '=', rec.device_input_id.id)],
                limit=rec.device_input_id.alarm_n,
                order='datetime_taken DESC')
            n_counter = 0
            for event in events:
                log_values = []
                if (rec.out_of_min_limit or rec.out_of_max_limit):
                    n_counter += 1
                    log_values.append(
                        [fields.Datetime.to_string(
                            fields.Datetime.context_timestamp(self,
                                                              event.datetime_taken)),
                         event.value])

            if n_counter > rec.device_input_id.alarm_c:
                items.append([rec.device_input_id.name, log_values])
        return items
