import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-iot",
    description="Meta package for oca-iot Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-iot',
        'odoo11-addon-iot_output',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
