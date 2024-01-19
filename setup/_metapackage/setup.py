import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-iot",
    description="Meta package for oca-iot Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-iot_input_oca>=16.0dev,<16.1dev',
        'odoo-addon-iot_oca>=16.0dev,<16.1dev',
        'odoo-addon-iot_output_oca>=16.0dev,<16.1dev',
        'odoo-addon-iot_template_oca>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
