# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class tsc_company_general_ledger_changes(models.Model):
#     _name = 'tsc_company_general_ledger_changes.tsc_company_general_ledger_changes'
#     _description = 'tsc_company_general_ledger_changes.tsc_company_general_ledger_changes'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
