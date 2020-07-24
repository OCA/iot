# Copyright 2020 Dimitrios Tanis <dtanis@tanisfood.gr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openupgradelib import openupgrade


def make_serials_unique(env):
    """
    Make serials unique by device by appending _1 to duplicates
    """
    env.cr.execute("""
    UPDATE iot_device_input
        SET serial = serial || '_1'
        WHERE iot_device_input.id IN
            (SELECT min(id)
            FROM iot_device_input
            GROUP BY device_id, serial
            HAVING count(*) > 1)
    """)


def set_dummy_passphrase(env):
    """
    Set dummy passphrase for inputs that don't have any
    """
    env.cr.execute("""
    UPDATE iot_device_input
        SET passphrase = 'change_me'
        WHERE passphrase IS NULL
    """)


@openupgrade.migrate()
def migrate(env, version):
    make_serials_unique(env)
    set_dummy_passphrase(env)
