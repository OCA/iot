There are two endpoints you can use:
Endpoint 1: /iot/<serial>/action

Takes `application/x-www-form-urlencoded` parameters:
passphase, value (where value is a JSON object)

1. Create a Device on `IoT > Config Devices`
2. Access the Inputs section of the device
3. Create an input. You must define a serial, passphrase, function and model

The function that the system will call must be of the following kind::

    @api.model
        def call_function(self, key):
        return {}

Where `key` is the input string send by the device and the result must be a dictionary
that will be responded to the device as a JSON.

Endpoint 2: /iot/<device_identification>/multi_input
It can be used to send values with multiple data in one POST request such as:
- Values for inputs of the same device with different address (multi input)
- Values for inputs of the same device with same address, different values (multi event)
- Mix of the above (multi input, multi event)

Takes `application/x-www-form-urlencoded` parameters:
passphase, values (a JSON array of JSON objects)

It is called using device_identification and passing two POST parameters: device passphrase and
a JSON string containing an array of values for input
- The value for the `address` key can be a string or a numeric (to conserve bytes in memory
restricted devices when creating the JSON object) and is converted to string when parsing.
- The value for the `value` key can either be string, number or boolean according to
JSON specs.
You can see an example of a valid JSON input object in the examples folder, using a few
combinations.

It requires the function that the system will call must be of the following kind::

    @api.model
        def call_function(self, key):
        'do something
        if err:
            return {'status': 'error', 'message': 'The error message you want to send to the device'}
        return {'status': 'ok', 'message': 'Optional success message'}

Where `key` is a dict send by the device having at least value for keys: 'address', 'value'

The function must always return a JSON with status and message. If value contains a value
with 'uuid' as key, it is returned along with the object for the IoT device to identify
success/failure per record.

It has full error reporting and the return value is a JSON array of dicts containing at
least status and message. Error message respose is at some points generic, though
extended logging is done in Odoo server logs.
