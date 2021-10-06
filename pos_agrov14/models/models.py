from odoo import models, fields, api

class PriceListMin(models.Model):
    _inherit = 'product.pricelist.item'
    x_price_min = fields.Float('Precio minimo',store=True)
    
    @api.depends('x_costo_promedio','x_tasa_utilidad')                               
    def _precio_sugerido(self):
        precio = 0
        for record in self:
            record['x_precio_sugerido'] = record.x_costo_promedio * (1+ record.x_tasa_utilidad/100)
            
    @api.onchange('fixed_price')
    def on_change_price(self):
        for record in self:
            if record.min_quantity == 1:
                record.product_tmpl_id['list_price'] = record.fixed_price
