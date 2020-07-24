# Copyright 2020 Dimitrios Tanis <dtanis@tanisfood.gr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

__name__ = "Upgrade to 12.0.1.1.0"


def _migrate_active(env):
    _logger.info("Setting all devices as active")
    env.cr.execute("""
        UPDATE iot_device
        SET active = TRUE;
    """)


def migrate(cr, version):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        _migrate_active(env)
