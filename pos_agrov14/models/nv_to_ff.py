# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from datetime import timedelta
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



class NvtoFFInvoice(models.Model):
    _inherit = 'account.move'
    x_ff = fields.Char('ff')

#    @api.one
#    def submit_application(self):
#        if self.x_ff == '/':
#            sequence_id = self.env['ir.sequence'].search([('code', '=', 'account.sequence.ff')])
#            sequence_pool = self.env['ir.sequence']
#            application_no = sequence_pool.sudo().get_id(sequence_id.id)
#            self.write({'x_ff': application_no})
#            self.write({'x_prueba': application_no})