from odoo import fields, models, api


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    week = fields.Integer(string="Week", compute="_compute_week")
    type_of_account = fields.Many2one( string="Type of Account", related="account_id.user_type_id")
    usd_amount = fields.Float(string="USD Amount", compute="_compute_expense_report_amount")
    bs_amount = fields.Float(string="Bs Amount", compute="_compute_expense_report_amount")

    @api.depends('date')
    def _compute_week(self):
        for record in self:
            if record.date:
                record.week = (record.date.day - 1) // 7 + 1
            else:
                record.week = 0


    @api.depends('amount_currency', 'currency_id', 'balance')
    def _compute_expense_report_amount(self):
        for record in self:
            if record.currency_id != record.company_currency_id:
                record.usd_amount = record.balance
                record.bs_amount = record.amount_currency
            else:
                record.usd_amount = record.amount_currency
                record.bs_amount = 0
