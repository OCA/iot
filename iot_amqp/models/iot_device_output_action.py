# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
import logging
_logger = logging.getLogger(__name__)
try:
    from pika import BlockingConnection, URLParameters, spec
except (ImportError, IOError) as err:
    _logger.debug(err)


class IotDeviceOutputAction(models.Model):
    _inherit = 'iot.device.output.action'

    def _run_amqp(self):
        url = self.output_id.amqp_host_id.connection
        connection = BlockingConnection(URLParameters(url))
        channel = connection.channel()
        result = channel.basic_publish(**self._generate_amqp_data())
        _logger.debug(result)
        connection.close()

    def _generate_amqp_data(self):
        return {
            'exchange': self.output_id.amqp_exchange,
            'routing_key': self.output_id.amqp_routing_key,
            'body': self.output_id.amqp_payload,
            'properties': spec.BasicProperties(),
            'mandatory': False
        }
