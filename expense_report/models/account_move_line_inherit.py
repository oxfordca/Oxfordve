from odoo import fields, models, api


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    week = fields.Integer(string="Week", compute="_compute_week")
    type_of_account = fields.Many2one( string="Type of Account", related="account_id.user_type_id")

    @api.depends('date')
    def _compute_week(self):
        for record in self:
            if record.date:
                record.week = (record.date.day - 1) // 7 + 1
            else:
                record.week = 0


