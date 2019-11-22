# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from mock import patch


class TestChannel:
    def __init__(self, test, output, *args, **kwargs):
        self.test = test
        self.output = output
        self.kwargs = kwargs
        self.args = args

    def basic_publish(
        self, exchange, routing_key, body, properties=None, mandatory=False
    ):
        self.test.assertEqual(exchange, self.output.amqp_exchange)
        self.test.assertEqual(routing_key, self.output.amqp_routing_key)
        self.test.assertEqual(body, self.output.amqp_payload)


class TestBlockingConnection:
    def __init__(self, test, output, *args, **kwargs):
        self.test = test
        self.output = output
        self.kwargs = kwargs
        self.args = args

    def connect(self, hostname, port, username, password):
        return

    def channel(self):
        return TestChannel(self.test, self.output, *self.args, **self.kwargs)

    def close(self):
        pass


class TestAmqp(TransactionCase):

    def setUp(self):
        super().setUp()
        self.host = self.env['iot.amqp.host'].create({
            'name': 'Host',
            'connection': 'amqp://demo_connection'
        })
        self.device = self.env['iot.device'].create({
            'name': 'Device',
        })
        self.system = self.env.ref('iot_amqp.amqp_system')
        self.output = self.env['iot.device.output'].create({
            'system_id': self.system.id,
            'device_id': self.device.id,
            'name': 'Output',
            'amqp_exchange': 'EXCHANGE',
            'amqp_routing_key': 'ROUTING_KEY',
            'amqp_host_id': self.host.id,
            'amqp_payload': "PAYLOAD",
        })

    def test_constrain_01(self):
        with self.assertRaises(ValidationError):
            self.output.amqp_exchange = False

    def test_constrain_02(self):
        with self.assertRaises(ValidationError):
            self.output.amqp_routing_key = False

    def test_constrain_03(self):
        with self.assertRaises(ValidationError):
            self.output.amqp_host_id = False

    def test_amqp(self):
        with patch(
            'odoo.addons.iot_amqp.models.iot_device_output_action.'
            'BlockingConnection'
        ) as mock:
            mock.return_value = TestBlockingConnection(self, self.output)
            self.output.with_context(
                iot_system_action_id=self.system.id,
            ).device_run_action()
            mock.assert_called()
