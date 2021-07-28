from odoo import models, fields, api

class PriceListMin(models.Model):
    _inherit = 'account.payment'
    x_monto_mn = fields.Char('Monto en Letra 00/100 MN', compute="_montomn", store=False)
    x_forma_de_pago = fields.Selection(selection = [('transferencia', 'Transferencia'), ('deposito', 'Deposito'),('cheque','Cheque'),], string =('Forma de pago'), store=True)
    x_folio_seguimiento = fields.Char('Folio de seguimiento', store=True)
    
    @api.depends('state')
    def _montomn(self):
        monto = self.amount
        if self.state == 'posted':
            self['x_monto_mn'] = self.currency_id.amount_to_text(int(monto)) + ' ' + str(
                int(round(monto - int(monto), 2) * 100)) + '/100 M.N.'
        else:
            self['x_monto_mn'] = 'CHEQUE CANCELADO'

            
class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    x_forma_de_pago = fields.Selection(selection = [('transferencia', 'Transferencia'), ('deposito', 'Deposito'),('cheque','Cheque'),], string =('Forma de pago'), store=True)
    x_folio_seguimiento = fields.Char('Folio de seguimiento', store=True)
