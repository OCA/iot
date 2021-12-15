import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-iot",
    description="Meta package for oca-iot Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-iot_amqp_oca',
        'odoo13-addon-iot_input_oca',
        'odoo13-addon-iot_oca',
        'odoo13-addon-iot_option_oca',
        'odoo13-addon-iot_output_oca',
        'odoo13-addon-iot_template_oca',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 13.0',
    ]
)
