import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-iot",
    description="Meta package for oca-iot Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-iot',
        'odoo12-addon-iot_amqp',
        'odoo12-addon-iot_input',
        'odoo12-addon-iot_option_oca',
        'odoo12-addon-iot_output',
        'odoo12-addon-iot_template_oca',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 12.0',
    ]
)
