# -*- coding: utf-8 -*-

from odoo import models, fields

class JournalType(models.Model):
    _inherit = 'account.journal' 

    is_custodian_type = fields.Boolean(
        string="¿Es de tipo custodio?",
        default = False
    )

    is_investment_type = fields.Boolean(
        string="¿Es de tipo inversión?",
        default = False
    )

class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    tsc_custom_domain = fields.Char(compute="_tsc_compute_custom_domain", search='_custom_domain_function', readonly=True, string="domain")

    def _tsc_compute_custom_domain(self):
        for record in self:
            record.tsc_custom_domain = ""

    def _custom_domain_function(self, operator, operand):

        custodian_journals = self.env['account.journal'].search([('is_custodian_type', '=', True)])
        investment_journals = self.env['account.journal'].search([('is_investment_type', '=', True)])

        custodian_journal_ids = custodian_journals.ids
        investment_journal_ids = investment_journals.ids

        group_custodian = self.env.user.has_group('restrict_journal_type.group_custodian_type_journal')
        group_investment = self.env.user.has_group('restrict_journal_type.group_investment_type_journal')

        if group_custodian and group_investment:
            return [('id', '!=', False)] 
        elif group_custodian and not group_investment:
            return[
                ('journal_id','not in',investment_journal_ids)
            ]
        elif not group_custodian and group_investment:
            return[
                ('journal_id','not in',custodian_journal_ids)
            ]
        else:
            return [
                ('journal_id', 'not in', custodian_journal_ids + investment_journal_ids)
            ]
        
class AccountJournalInherit(models.Model):
    _inherit = 'account.journal'

    tsc_custom_domain_journal = fields.Char(compute="_tsc_compute_custom_domain_journal", search='_custom_domain_function_journal', readonly=True, string="domain")

    def _tsc_compute_custom_domain_journal(self):
        for record in self:
            record.tsc_custom_domain_journal = ""

    def _custom_domain_function_journal(self, operator, operand):

        custodian_journals = self.env['account.journal'].search([('is_custodian_type', '=', True)])
        investment_journals = self.env['account.journal'].search([('is_investment_type', '=', True)])

        custodian_journal_ids = custodian_journals.ids
        investment_journal_ids = investment_journals.ids

        group_custodian = self.env.user.has_group('restrict_journal_type.group_custodian_type_journal')
        group_investment = self.env.user.has_group('restrict_journal_type.group_investment_type_journal')

        if group_custodian and group_investment:
            return [('id', '!=', False)] 
        elif group_custodian and not group_investment:
            return[
                ('id','not in',investment_journal_ids)
            ]
        elif not group_custodian and group_investment:
            return[
                ('id','not in',custodian_journal_ids)
            ]
        else:
            return [
                ('id', 'not in', custodian_journal_ids + investment_journal_ids)
        ]

    tsc_custom_domain_journal_negation = fields.Char(compute="_tsc_compute_custom_domain_journal_negation", search='_custom_domain_function_journal_negation', readonly=True, string="domain")

    def _tsc_compute_custom_domain_journal_negation(self):
        for record in self:
            record.tsc_custom_domain_journal_negation = ""

    def _custom_domain_function_journal_negation(self, operator, operand):

        custodian_journals = self.env['account.journal'].search([('is_custodian_type', '=', True)])
        investment_journals = self.env['account.journal'].search([('is_investment_type', '=', True)])

        custodian_journal_ids = custodian_journals.ids
        investment_journal_ids = investment_journals.ids

        group_custodian = self.env.user.has_group('restrict_journal_type.group_custodian_type_journal')
        group_investment = self.env.user.has_group('restrict_journal_type.group_investment_type_journal')

        if group_custodian and group_investment:
           return [
                ('id', 'in', custodian_journal_ids + investment_journal_ids)
           ]
        elif group_custodian and not group_investment:
            return[
                ('id','in',custodian_journal_ids)
            ]
        elif not group_custodian and group_investment:
            return[
                ('id','in',investment_journal_ids)
            ]
        else:
            return [('id', '=', False)] 
            
class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    tsc_custom_domain_journal_line = fields.Char(compute="_tsc_compute_custom_domain_journal_line", search='_custom_domain_function_journal_line', readonly=True, string="domain")


    def _tsc_compute_custom_domain_journal_line(self):
        for record in self:
            record.tsc_custom_domain_journal_line = ""

    def _custom_domain_function_journal_line(self, operator, operand):

        custodian_journals = self.env['account.journal'].search([('is_custodian_type', '=', True)])
        investment_journals = self.env['account.journal'].search([('is_investment_type', '=', True)])

        custodian_journal_ids = custodian_journals.ids
        investment_journal_ids = investment_journals.ids

        group_custodian = self.env.user.has_group('restrict_journal_type.group_custodian_type_journal')
        group_investment = self.env.user.has_group('restrict_journal_type.group_investment_type_journal')

        if group_custodian and group_investment:
            return [('id', '!=', False)] 
        elif group_custodian and not group_investment:
            return[
                ('journal_id','not in',investment_journal_ids)
            ]
        elif not group_custodian and group_investment:
            return[
                ('journal_id','not in',custodian_journal_ids)
            ]
        else:
            return [
                ('journal_id', 'not in', custodian_journal_ids + investment_journal_ids)
            ]

