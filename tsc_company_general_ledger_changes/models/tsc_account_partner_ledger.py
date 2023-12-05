# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.misc import format_date


class AccountPartnerLedger(models.AbstractModel):

    _inherit = "account.partner.ledger"
    
    def _get_columns_name(self, options):

        res = super(AccountPartnerLedger, self)._get_columns_name(options)
        res.insert(5, {'name': _('Estimated Reception')}) 
        res.insert(6, {'name': _('Prod Received?')}) 
        res.insert(7, {'name': _('In transit?')}) 

        return res
    
    def _get_report_line_move_line(self, options, partner, aml, cumulated_init_balance, cumulated_balance):

        res = super(AccountPartnerLedger, self)._get_report_line_move_line(options, partner, aml, cumulated_init_balance, cumulated_balance)
        
        aml_id = self.env['account.move.line'].browse(int(aml['id']))

        if aml_id.move_id.invoice_origin and aml_id.move_id.move_type == 'in_invoice':

            po_obj = self.env['purchase.order'].search([('name', '=', aml_id.move_id.invoice_origin)])

            if po_obj:
                date_planned = po_obj.date_planned and format_date(self.env, fields.Date.from_string(po_obj.date_planned))
                is_shipped = _('Yes') if po_obj.is_shipped else _('No')
                tsc_is_transit = _('Yes') if po_obj.tsc_is_transit else _('No')

                res['columns'].insert(4, {'name': date_planned, 'class': 'date'})
                res['columns'].insert(5, {'name': is_shipped})
                res['columns'].insert(6, {'name': tsc_is_transit})

            for item in res['columns']:
                if 'class' in item and item['class'] == 'o_account_report_line_ellipsis':

                    if po_obj.tsc_is_transit and aml_id.move_id.payment_state == 'not_paid':
                        item['class'] = 'o_account_report_line_ellipsis text-danger'

                    if not po_obj.tsc_is_transit and not po_obj.is_shipped:
                        item['class'] = 'o_account_report_line_ellipsis text-success'

        else:
            
            res['columns'].insert(4, {'name': ''})
            res['columns'].insert(5, {'name': ''})
            res['columns'].insert(6, {'name': ''})

        return res
    
    def _get_report_line_partner(self, options, partner, initial_balance, debit, credit, balance):

        res = super(AccountPartnerLedger, self)._get_report_line_partner(options, partner, initial_balance, debit, credit, balance)

        res['colspan'] = 9

        return res
    
    def _get_report_line_total(self, options, initial_balance, debit, credit, balance):

        res = super(AccountPartnerLedger, self)._get_report_line_total(options, initial_balance, debit, credit, balance)

        res['colspan'] = 9

        return res
