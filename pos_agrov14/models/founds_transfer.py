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

class FoundsTransfer(models.Model):
    _inherit = "account.payment"

    def transfer_payments_action(self):
        x = self.env['account.journal'].search([('bank_account_id','=',self.partner_bank_id.acc_number)])
        self.x_prueba = x.name

    def _create_basic_move(self, cred_account=None, deb_account=None, amount=0, date_str='2019-02-01',
                           partner_id=False, name=False, cred_analytic=False, deb_analytic=False,
                           transfer_model_id=False, journal_id=False, posted=True):
        move_vals = {
            'date': date_str,
            'transfer_model_id': transfer_model_id,
            'line_ids': [
                (0, 0, {
                    'account_id': cred_account or self.origin_accounts[0].id,
                    'credit': amount,
                    'analytic_account_id': cred_analytic,
                    'partner_id': partner_id,
                }),
                (0, 0, {
                    'account_id': deb_account or self.origin_accounts[1].id,
                    'analytic_account_id': deb_analytic,
                    'debit': amount,
                    'partner_id': partner_id,
                }),
            ]
        }
        if journal_id:
            move_vals['journal_id'] = journal_id
        move = self.env['account.move'].create(move_vals)
        if posted:
            move.action_post()
        return move

