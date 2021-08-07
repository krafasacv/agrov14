from odoo import models, fields, api

class PriceListMin(models.Model):
    _inherit = 'res.partner'
    x_birthday = fields.Date('Fecha de Cumpleaños',store=True)



