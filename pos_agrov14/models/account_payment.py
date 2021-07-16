from odoo import models, fields, api

class PriceListMin(models.Model):
    _inherit = 'account.payment'
    x_monto_mn = fields.Char('Monto en Letra 00/100 MN', compute="_montomn", store=False)

    @api.depends('state')
    def _montomn(self):
        monto = self.amount
        if self.state == 'posted':
            self['x_monto_mn'] = self.currency_id.amount_to_text(int(monto)) + ' ' + str(
                int(round(monto - int(monto), 2) * 100)) + '/100 M.N.'
        else:
            self['x_monto_mn'] = 'CHEQUE CANCELADO'
