from odoo import models, fields, api

class PriceListMin(models.Model):
    _inherit = 'account.move.line'
    x_bt_cj = fields.Char('Cj/Bt',store=True)



