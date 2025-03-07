from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class FilterDateWizard(models.TransientModel):
    _name = 'filter.date.wizard'
    _description = 'Filter Date Wizard'

    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)

    @api.constrains('date_from', 'date_to')
    def _check_date_range(self):
        for rec in self:
            if rec.date_from and rec.date_to and rec.date_from > rec.date_to:
                raise ValidationError(_("The 'From' date cannot be later than the 'To' date."))

    def filter_date_wizard_action_confirm(self):
        active_domain = self.env.context.get('active_domain', [])

        cleaned_active_domain = []
        for condition in active_domain:
            if isinstance(condition, (tuple, list)):
                if condition and condition[0] == 'date' and condition[1] in ['>=', '<=']:
                    continue
            cleaned_active_domain.append(condition)

        wizard_domain = []
        if self.date_from:
            wizard_domain.append(('date', '>=', self.date_from))
        if self.date_to:
            wizard_domain.append(('date', '<=', self.date_to))

        combined_domain = cleaned_active_domain + wizard_domain

        return {
            'type': 'ir.actions.act_window',
            'name': _('Expense Report'),
            'res_model': 'account.move.line',
            'view_mode': 'tree',
            'view_id': self.env.ref('expense_report.view_expense_report_tree').id,
            'domain': combined_domain,
            'target': 'current',
        }
