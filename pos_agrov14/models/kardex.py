from odoo import models, fields, api

class PriceListMin(models.Model):
    _inherit = 'stock.move.line'
    x_costo_generado = fields.Float(string='Costo', related='move_id.price_unit')

