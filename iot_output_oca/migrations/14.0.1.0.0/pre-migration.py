# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade

_column_renames = {
    "iot_device_output": [("system_id", "communication_system_id")],
    "iot_device_output_action": [
        ("system_action_id", "communication_system_action_id")
    ],
}


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_columns(env.cr, _column_renames)
