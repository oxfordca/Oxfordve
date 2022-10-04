# -*- coding: utf-8 -*-


from odoo import models, fields, api, exceptions


class AccountBankStatementInherit(models.Model):
    _inherit = 'account.bank.statement'
#     _description = 'name.name'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#    @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

    @api.model
    def create(self, vals):   
        
        res = super(AccountBankStatementInherit,self).create(vals)
        u = self.env['res.users'].search([('id', '=', self.env.uid)])
        if(not u.has_group('restrictions_for_bank_statements_and_reconciliation.group_crear_e_importar_extractos_bancarios')):
           raise exceptions.UserError('No tienes permiso para crear extractos bancarios.')    

        return res