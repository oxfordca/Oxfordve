# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class tsc_AccountMove(models.Model):

    _inherit = 'account.move'

    @api.model
    def _create(self, data_list):
        for data in data_list:
            stored = data["stored"]
            if stored.get("move_type") in {'out_invoice', 'out_refund', 'out_receipt'}:
                branch_id = stored.get("branch_id")
                if branch_id:
                    journal = self.env["account.journal"].search(
                        [("branch_id", "=", branch_id)], limit=1)
                    if journal.id:
                        stored["journal_id"] = journal.id
        return super()._create(data_list)

    @api.depends('company_id', 'invoice_filter_type_domain')
    def _compute_suitable_journal_ids(self):
        for m in self:
            journal_type = m.invoice_filter_type_domain or 'general'
            company_id = m.company_id.id or self.env.company.id
            branch_id = self.env.user.branch_id.id
            domain = [('company_id', '=', company_id), 
                      ('type', '=', journal_type),
                      '|',
                      ('branch_id','=',False),
                      ('branch_id','=',branch_id)]
            m.suitable_journal_ids = self.env['account.journal'].search(domain)
            
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = domain or []
        tsc_default_move_type = self.env.context.get('default_move_type')
        if tsc_default_move_type in ['out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'entry']:
            domain.extend(['|', ('branch_id','=',False),
                       ('branch_id','=',self.env.user.branch_id.id)])
        return super(tsc_AccountMove, self).search_read(domain, fields, offset, limit, order)

    @api.model
    def _search_default_journal(self, journal_types):
        company_id = self._context.get('default_company_id', self.env.company.id)
        branch_id = self.env.user.branch_id.id
        domain = [('company_id', '=', company_id), 
                  ('type', 'in', journal_types), 
                  '|',
                  ('branch_id','=',False),
                  ('branch_id','=',branch_id)]

        journal = None
        if self._context.get('default_currency_id'):
            currency_domain = domain + [('currency_id', '=', self._context['default_currency_id'])]
            journal = self.env['account.journal'].search(currency_domain, limit=1)

        if not journal:
            journal = self.env['account.journal'].search(domain, limit=1)

        if not journal:
            company = self.env['res.company'].browse(company_id)

            error_msg = _(
                "No journal could be found in company %(company_name)s for any of those types: %(journal_types)s",
                company_name=company.display_name,
                journal_types=', '.join(journal_types),
            )
            raise UserError(error_msg)

        return journal


class tsc_AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = domain or []        
        tsc_journal_type = self.env.context.get('journal_type')
        tsc_search_default_posted = self.env.context.get('search_default_posted') 
        if tsc_journal_type in ['sales', 'general', 'purchase', 'bank'] and tsc_search_default_posted == 1:
            domain.extend(['|', ('branch_id','=',False),
                       ('branch_id','=',self.env.user.branch_id.id)])
        return super(tsc_AccountMoveLine, self).search_read(domain, fields, offset, limit, order)

