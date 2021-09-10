# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from datetime import timedelta,datetime
from functools import partial

import psycopg2
import pytz

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero, float_round
from odoo.exceptions import ValidationError, UserError
from odoo.http import request
from odoo.osv.expression import AND
import base64

_logger = logging.getLogger(__name__)

class NvPosInvoice(models.Model):
    _inherit = 'account.move'
##este campo tal vez no sea necesario porque en el mismo procedimiento se estan marcando las notas de venta afectadas.
    x_nv_origen = fields.Char('Notas de Venta de Origen',readonly=True)
################
    x_nv_destino = fields.Char('Nota de Venta Destino', readonly=True)
           
#este procedimiento es para agrupar varias notas de venta en una sola factura
    def action_many_nv_one_invoice(self): 
        invoice_vals = {}
        ref = ''
        refa = ''
        cia = self.company_id.id
        self_ids = self.filtered(lambda r: r.payment_state in ['in_payment','paid'] and r.x_nv_destino == False).ids 
        #Se agrega r.x_nv_destino para evitar que se vuelvan a agrupar
        self.x_nv_origen = self_ids
        
        ######
        fp = '04'
        ffff = ''
        for rec in self.filtered(lambda r: r.payment_state in ['in_payment','paid']):
            ffff = rec.payment_id
            if rec.payment_id.x_forma_de_pago == 'transferencia':
                fp = '03'
            elif rec.payment_id.x_forma_de_pago == 'deposito':
                fp = ''
            elif rec.payment_id.x_forma_de_pago == 'cheque':
                fp = '02'
            else:
                fp = '01'
          ######    
            
            
        lineas = self.env['account.move.line'].search([('move_id', 'in', self_ids)]).filtered(lambda r: r.product_id and r.is_anglo_saxon_line != True) 
        # se agrega r.is_anglo_saxon_line, para evitar que el sistema mande partidas como el costo de venta
        list_lin = []
        nv_ids = []
        for linea in lineas.sorted(key=lambda r: r.move_id.id):
            if refa != linea.move_id.name:
                ref += linea.move_id.name + ' '
                refa = linea.move_id.name
                nv_ids.append(linea.move_id.id)

            list_lin.append((0, 0,
             {'ref': linea.move_id.name,
                  'journal_id': 1, #el Id es 10 para que se generen el el POS de lo contrario hay que poner el 1
                  'company_id': cia,
                  'company_currency_id': 33,
                  'account_id': linea.product_id.product_tmpl_id.categ_id.property_account_income_categ_id.id,
                  'account_root_id': linea.product_id.product_tmpl_id.categ_id.property_account_income_categ_id.root_id.id,
                  'name': linea.name,
                  'quantity': linea.quantity,
                  'price_unit': linea.price_unit,
                  'product_uom_id': linea.product_uom_id.id,
                  'product_id': linea.product_id.id,
                  'tax_ids': [(6, 0, linea.tax_ids.ids)]
              }))

        invoice_vals = {
                'journal_id': 1, #el Id es 10 para que se generen el el POS de lo contrario hay que poner el 1
                'move_type': 'out_invoice',
                'invoice_origin': self.ids,
                'company_id': cia,
                'partner_id': self.partner_id.id,
                'partner_shipping_id': self.partner_id.id,
                'currency_id': self.currency_id.id,
                'payment_reference': ref,
                'invoice_payment_term_id': 1,
                'team_id': 1,
                'invoice_line_ids': list_lin,
                'forma_pago': fp,#'01', #este dato debe venir de la plantilla del cliente
                'methodo_pago': 'PUE', #este dato debe venir de la plantilla del cliente
                'uso_cfdi': 'P01', #este dato debe venir de la plantilla del cliente
                'tipo_comprobante': 'I',
                'state': 'draft',
                'x_prueba': ffff,
            }
    
        new = self.env['account.move'].sudo().create(invoice_vals)
        new.state = 'posted'
        new.x_nv_origen = self_ids
        
        for rec in self.filtered(lambda r: r.payment_state in ['in_payment','paid']):
            rec.x_nv_destino = new.name
        
#Estas líneas so para asignar un folio unico a las facturas tal vez para las que ya están timbradas
#        if new.x_ff == '/':
#            sequence_id = self.env['ir.sequence'].search([('code', '=', 'account.sequence.ff')])
#            sequence_pool = self.env['ir.sequence']
#            application_no = sequence_pool.sudo().get_id(sequence_id.id)
#            new.write({'x_ff': application_no})
#            prefijo_secuencia = new.sequence_prefix
#            new.name = new.x_ff
#            new.sequence_prefix = prefijo_secuencia
#aqui termina la asignación del folio unico para las facturas, hay que checar si se puede asignar al nombre del documento sin que afecte a la secuncia nativa de Odoo y checar si al timbrar toma este dato.
        
        
        new.PostoInvoiceReversal()
        return(invoice_vals)    
                                
