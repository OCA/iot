# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """SELECT id, device_identification, passphrase
        FROM iot_device
        WHERE device_identification IS NOT NULL""",
    )
    res = env.cr.fetchall()
    for device_id, serial, passphrase in res:
        env["iot.device.input"].create(
            {
                "device_id": device_id,
                "serial": serial,
                "passphrase": passphrase,
                "name": "Multi value input - Generated on Migration",
                "call_function": "parse_multi_input",
            }
        )
