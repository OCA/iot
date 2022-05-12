import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-iot",
    description="Meta package for oca-iot Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-iot_input_oca>=15.0dev,<15.1dev',
        'odoo-addon-iot_oca>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
