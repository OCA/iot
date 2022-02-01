import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class IotDevice(models.Model):
    _inherit = 'iot.device'

    input_ids = fields.One2many(
        'iot.device.input',
        inverse_name='device_id'
    )
    input_count = fields.Integer(compute='_compute_input_count')

    @api.depends('input_ids')
    def _compute_input_count(self):
        for r in self:
            r.input_count = len(r.input_ids)

    @api.multi
    def action_show_input(self):
        self.ensure_one()
        action = self.env.ref('iot_input.iot_device_input_action')
        result = action.read()[0]

        result['context'] = {
            'default_device_id': self.id,
        }
        result['domain'] = "[('device_id', '=', " + \
                           str(self.id) + ")]"
        if len(self.input_ids) == 1:
            result['views'] = [(False, 'form')]
            result['res_id'] = self.input_ids.id
        return result

    @api.multi
    def parse_single_input(self, value):
        '''Handle single input for device

        :param dict value:
            Dict containing at least keys 'address', 'value'
        :returns: dict with keys 'status', 'message' where:
            - status='ok' when value is parsed without errors
            - status='error' and message='error message' when error occurs
            If value contains a value with key 'uuid', it is passed in the return dict
            to identify result for each entry at the iot end
        :rtype: dict
        '''
        if 'address' not in value.keys():
            _logger.warning('Address for Input is required')
            msg = {'status': 'error',
                   'message': _('Address for Input is required')}
            if 'uuid' in value.keys():
                msg['uuid'] = value['uuid']
            return msg
        if 'value' not in value.keys():
            _logger.warning('Value for Input is required')
            msg = {'status': 'error',
                   'message': _('Value for Input is required')}
            if 'uuid' in value.keys():
                msg['uuid'] = value['uuid']
            return msg

        device_input = self.input_ids.filtered(lambda i: i.address == value['address'])
        if len(device_input) == 1:
            res = device_input._call_device(value)
            self.env['iot.device.input.action'].create(
                device_input._add_action_vals(value, res))
            if 'uuid' in value:
                res['uuid'] = value['uuid']
            return res
        else:
            _logger.warning('Input with address %s not found', value['address'])
            msg = {'status': 'error',
                   'message': _('Server Error. Check server logs')}
            if 'uuid' in value:
                msg['uuid'] = value['uuid']
            return msg

    @api.model
    def parse_multi_input(self, device_identification, passphrase, values):
        '''Handle multiple inputs for device

        :param string device_identification:
            Device identification.
        :param string passphrase:
            Device passphrase.
        :param list values:
            Values is a list of dicts with at least values for keys 'address', 'value'
            Each dict in the list can have:
             - Different address (multi input)
             - Same address, different values (multi event)
             - Mix of the above (multi input, multi event)
        :returns: JSON encodable list of dicts
        :rtype: list
        '''
        device = self.with_context(
            active_test=False).search(
                [('device_identification', '=', device_identification)])
        if not device:
            _logger.warning(
                'Device with identification %s not found',
                device_identification)
            return {'status': 'error',
                    'message': _('Server Error. Check server logs')}
        if not device.active:
            _logger.warning(
                'Device with identification %s is inactive, no data will be logged',
                device.device_identification)
            return {'status': 'error',
                    'message': _('Server Error. Check server logs')}
        if device.passphrase != passphrase:
            _logger.warning(
                'Wrong passphrase for device with identification %s',
                device.device_identification)
            return {'status': 'error',
                    'message': _('Server Error. Check server logs')}

        if not values:
            _logger.warning(
                'Empty values array for device with identification %s',
                device.device_identification)
            return {'status': 'error',
                    'message': _('Empty values array')}
        res = []
        for d in values:
            res.append(device.parse_single_input(d))
        return res
