from odoo import models, fields, api

class PriceListMin(models.Model):
    _inherit = 'stock.move.line'
    x_costo_generado = fields.Float(string='Costo', related='move_id.price_unit')
    x_origen = fields.Integer(string='Origen', related='move_id.location_id.id', readonly = True, storage= True)
    x_entrada_salida = fields.Char(string='Entrada/Salida', readonly = True)
