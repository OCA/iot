# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade

_model_renames = [
    ("iot.system", "iot.communication.system"),
    ("iot.system.action", "iot.communication.system.action"),
]

_table_renames = [
    ("iot_system", "iot_communication_system"),
    ("iot_system_action", "iot_communication_system_action"),
]

_column_renames = {
    "iot_communication_system_action": [("system_id", "communication_system_id")],
    "iot_device": [("system_id", "communication_system_id")],
    "iot_device_action": [("system_action_id", "communication_system_action_id")],
}


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_models(env.cr, _model_renames)
    openupgrade.rename_tables(env.cr, _table_renames)
    openupgrade.rename_columns(env.cr, _column_renames)
