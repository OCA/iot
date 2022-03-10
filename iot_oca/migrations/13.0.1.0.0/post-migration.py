# Copyright 2022 ForgeFlow
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def fix_iot_device_image(env):
    IOTDevice = env["iot.device"]
    attachments = env["ir.attachment"].search(
        [
            ("res_model", "=", "iot.device"),
            ("res_field", "=", "image"),
            ("res_id", "!=", False),
        ]
    )
    for attachment in attachments:
        IOTDevice.browse(attachment.res_id).image_1920 = attachment.datas


@openupgrade.migrate()
def migrate(env, version):
    fix_iot_device_image(env)
