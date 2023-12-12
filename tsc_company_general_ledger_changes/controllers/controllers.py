# -*- coding: utf-8 -*-
# from odoo import http


# class TscCompanyGeneralLedgerChanges(http.Controller):
#     @http.route('/tsc_company_general_ledger_changes/tsc_company_general_ledger_changes', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tsc_company_general_ledger_changes/tsc_company_general_ledger_changes/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tsc_company_general_ledger_changes.listing', {
#             'root': '/tsc_company_general_ledger_changes/tsc_company_general_ledger_changes',
#             'objects': http.request.env['tsc_company_general_ledger_changes.tsc_company_general_ledger_changes'].search([]),
#         })

#     @http.route('/tsc_company_general_ledger_changes/tsc_company_general_ledger_changes/objects/<model("tsc_company_general_ledger_changes.tsc_company_general_ledger_changes"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tsc_company_general_ledger_changes.object', {
#             'object': obj
#         })
