from odoo import models, fields, api

class PriceListMin(models.Model):
    _inherit = 'res.partner'
    
    
    
    #x_cumple = fields.Char('cumple', store=True)
    
    x_metodo_pago = fields.Selection(
        [('PUE', 'PUE - Pago en una sola exhibición'), ('PPD', 'PPD - Pago en parcialidades o diferido'), ],
        string='Método de pago', )
    
    x_forma_pago = fields.Selection([('01', '01 - Efectivo'),
                                    ('02', '02 - Cheque nominativo'),
                                    ('03', '03 - Transferencia electrónica de fondos'),
                                    ('04', '04 - Tarjeta de Crédito'),
                                    ('05', '05 - Monedero electrónico'),
                                    ('06', '06 - Dinero electrónico'),
                                    ('08', '08 - Vales de despensa'),
                                    ('12', '12 - Dación en pago'),
                                    ('13', '13 - Pago por subrogación'),
                                    ('14', '14 - Pago por consignación'),
                                    ('15', '15 - Condonación'),
                                    ('17', '17 - Compensación'),
                                    ('23', '23 - Novación'),
                                    ('24', '24 - Confusión'),
                                    ('25', '25 - Remisión de deuda'),
                                    ('26', '26 - Prescripción o caducidad'),
                                    ('27', '27 - A satisfacción del acreedor'),
                                    ('28', '28 - Tarjeta de débito'),
                                    ('29', '29 - Tarjeta de servicios'),
                                    ('30', '30 - Aplicación de anticipos'),
                                    ('31', '31 - Intermediario pagos'),
                                    ('99', '99 - Por definir'), ], string='Forma de pago', )
    
    x_regimen_fiscal = fields.Selection(
        selection=[('601', _('General de Ley Personas Morales')),
                   ('603', _('Personas Morales con Fines no Lucrativos')),
                   ('605', _('Sueldos y Salarios e Ingresos Asimilados a Salarios')),
                   ('606', _('Arrendamiento')),
                   ('608', _('Demás ingresos')),
                   ('609', _('Consolidación')),
                   ('610', _('Residentes en el Extranjero sin Establecimiento Permanente en México')),
                   ('611', _('Ingresos por Dividendos (socios y accionistas)')),
                   ('612', _('Personas Físicas con Actividades Empresariales y Profesionales')),
                   ('614', _('Ingresos por intereses')),
                   ('616', _('Sin obligaciones fiscales')),
                   ('620', _('Sociedades Cooperativas de Producción que optan por diferir sus ingresos')),
                   ('621', _('Incorporación Fiscal')),
                   ('622', _('Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras')),
                   ('623', _('Opcional para Grupos de Sociedades')),
                   ('624', _('Coordinados')),
                   ('628', _('Hidrocarburos')),
                   ('607', _('Régimen de Enajenación o Adquisición de Bienes')),
                   ('629', _('De los Regímenes Fiscales Preferentes y de las Empresas Multinacionales')),
                   ('630', _('Enajenación de acciones en bolsa de valores')),
                   ('615', _('Régimen de los ingresos por obtención de premios')),
                   ('625', _('Régimen de las Actividades Empresariales con ingresos a través de Plataformas Tecnológicas')),
                   ('626', _('Régimen Simplificado de Confianza')),],
        string=_('Régimen Fiscal'), 
    )



