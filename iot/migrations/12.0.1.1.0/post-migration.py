# Copyright 2020 Dimitrios Tanis <dtanis@tanisfood.gr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openupgradelib import openupgrade


def _migrate_active(env):
    """
    Set all device inputs as active
    """
    env.cr.execute("""
        UPDATE iot_device
        SET active = TRUE;
    """)


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    _migrate_active(env)
