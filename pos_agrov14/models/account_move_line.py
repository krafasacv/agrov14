from odoo import models, fields, api

class account_move_line(models.Model):
    _inherit = 'account.move.line'
    x_bt_cj = fields.Char('Cj/Bt',store=True)
    x_prueba = fields.Char('prueba',store=True)



        



