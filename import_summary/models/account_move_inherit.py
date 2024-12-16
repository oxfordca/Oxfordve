from odoo import fields, models, api


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    importation_check = fields.Boolean(string="Importation", compute='_compute_importation_check', inverse='_inverse_importation_check', store=True)

    @api.depends('move_type')
    def _compute_importation_check(self):
        for record in self:
            if record.move_type == 'in_invoice' and not record.debit_origin_id and record.state != 'posted':
                record.importation_check = True
            else:
                record.importation_check = False

    def _inverse_importation_check(self):
        for record in self:
            if record.move_type != 'in_invoice' or record.debit_origin_id:
                record.importation_check = False

    # Override action_post method to create import summary
    def action_post(self):
        res = super(AccountMoveInherit, self).action_post()
        for record in self:
            if record.importation_check:
                self.env['import.summary'].create_import_summary(record)
            else:
                self.env['import.summary'].delete_import_summary(record)
        return res