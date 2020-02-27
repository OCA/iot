# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import traceback
from io import StringIO
import logging
from odoo import fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IoTSystemAction(models.Model):
    _name = 'iot.system.action'
    _description = 'IoT System.action'

    name = fields.Char(required=True)
    system_id = fields.Many2one('iot.system', required=True)

    def _run(self, device_action):
        raise ValidationError(_('Action cannot be processed'))

    def run(self, device_action):
        try:
            result = self._run(device_action)
            return 'ok', result
        except Exception:
            buff = StringIO()
            traceback.print_exc(file=buff)
            error = buff.getvalue()
            _logger.warning(error)
            return 'failed', error
