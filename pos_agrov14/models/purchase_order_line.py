from odoo import models, fields, api

class account_move_line(models.Model):
    _inherit = 'purchase.order.line'
    x_bt_cj = fields.Char('Cj/Bt',store=True)
    
    


        



