from odoo import models, fields, api

class PriceListMin(models.Model):
    _inherit = 'product.pricelist.item'
    x_price_min = fields.Float('Precio minimo',store=True)



