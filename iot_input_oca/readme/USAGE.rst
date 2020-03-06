1. Create a Device on `IoT > Config Devices`
2. Access the Inputs section of the device
3. Create an input. You must define a serial, passphrase, function and model

The function that the system will call must be of the following kind::

    @api.model
        def call_function(self, key):
        return {}

Where `key` is the input string send by the device and the result must be a dictionary
that will be responded to the device as a JSON.
