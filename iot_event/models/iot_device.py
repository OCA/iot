# Copyright (C) 2020 Dimitrios Tanis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import pytz

from odoo import fields, models


# put POSIX 'Etc/*' entries at the end to avoid confusing users - see bug 1086728
_tzs = [(tz, tz) for tz in sorted(
    pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]


def _tz_get(self):
    return _tzs


class IotDevice(models.Model):
    _inherit = 'iot.device'

    time_source = fields.Selection(
        selection=[
            ("device", "Device Time"),
            ("server", "Server Time"),
        ],
        default="device",
        required=True,
        help="Time source used when logging datetime for event."
        "- Device Time: Datetime is recorded as sent from device in POST request"
        "- Server Time: Datetime from server when POST request is proccessed"
        "(used when device doesn't have RTC)",
    )
    tz = fields.Selection(
        _tz_get, string='Timezone', default=lambda self: self._context.get('tz'),
        help="The devices's timezone, used to output proper date and time values "
             "in events where device does not have a RTC")
