# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class tsc_AccountPayment(models.Model):

    _inherit = 'account.payment'

    def tsc_compute_tsc_journal_ids(self):
        return self.tsc_get_filtered_journals()

    tsc_journal_ids = fields.Many2many('account.journal', string='Branch-filtered Journals', 
                                       store=False, readonly=False,
                                       default=tsc_compute_tsc_journal_ids)

    def tsc_get_filtered_journals(self):
        return self.env['account.journal'].search([
                    ('type', 'in', ('bank', 'cash')),
                    ('company_id', '=', self.env.context['allowed_company_ids'][0]),
                    '|',
                     ('branch_id','=',False),
                     ('branch_id','=',self.env.user.branch_id.id)
                 ])

    def tsc_get_default_journal(self):
        tsc_journals = self.tsc_get_filtered_journals()
        return tsc_journals[0] if len(tsc_journals) else False


    journal_id = fields.Many2one(related='move_id.journal_id', store=True, index=True, copy=False, default=tsc_get_default_journal)

class tsc_AccountPaymentRegister(models.TransientModel):

    _inherit = 'account.payment.register'

    def tsc_compute_tsc_journal_ids(self):
        return self.tsc_get_filtered_journals()

    tsc_journal_ids = fields.Many2many('account.journal', string='Branch-filtered Journals', 
                                       store=False, readonly=False,
                                       default=tsc_compute_tsc_journal_ids)

    def tsc_get_filtered_journals(self):
        return self.env['account.journal'].search([
                    ('type', 'in', ('bank', 'cash')),
                    ('company_id', '=', self.env.context['allowed_company_ids'][0]),
                    '|',
                     ('branch_id','=',False),
                     ('branch_id','=',self.env.user.branch_id.id)
                 ])

    




