import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-iot",
    description="Meta package for oca-iot Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-iot_oca',
        'odoo14-addon-iot_output_oca',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
