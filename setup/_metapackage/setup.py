import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-iot",
    description="Meta package for oca-iot Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-iot',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
