from odoo import api, models, fields, _
from odoo.exceptions import UserError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    @api.model
    def create(self, vals):
        quotation = super(SaleOrderInherit, self).create(vals)
        if quotation.partner_id:
            sales_man = quotation.partner_id.user_id
            if sales_man:
                if user.login:
                    try:
                        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                        url = f"{base_url}/web#id={quotation.id}&menu_id=178&model=sale.order&view_type=form"
                        email_values = {
                            'author_id': self.env.user.id,
                            'email_to': sales_man.login,
                            'subject': _('New Quotation: %s') % quotation.name,
                            'body_html': _(
                                """
                                <p>There is a new quotation waiting for you.</p>
                                <p>Click <a href="%s">here</a> to see it.</p>
                                <p>Sincerely,</p>
                                <p>Your Odoo System</p>
                                """ % url
                            ),
                        }
                        mail_mail = self.env['mail.mail'].create(email_values)
                        mail_mail.send()
                    except Exception as e:
                        raise UserError(_("Error sending email notification: %s") % str(e))
            else:
                _logger.warning("No user found associated with partner %s (ID: %s) for quotation %s (ID: %s)",
                                quotation.partner_id.name, quotation.partner_id.id, quotation.name, quotation.id)
        return quotation