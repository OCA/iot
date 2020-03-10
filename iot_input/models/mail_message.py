from odoo import api, models, _


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, vals):
        device = self.env.context.get('iot_device_name', False)
        if device:
            body = vals.get('body', '')
            if len(body) > 0:
                body += '<br>'
            vals['body'] = '%s%s' % (
                body, _('Detected automatically by %s') % device)
        return super().create(vals)
