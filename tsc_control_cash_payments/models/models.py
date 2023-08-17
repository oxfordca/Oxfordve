# -*- coding: utf-8 -*-

from odoo import _, api, exceptions, fields, models
from odoo.exceptions import UserError

class TSCAccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    @api.depends('company_id')
    def tsc_journal_domain(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])

        if res_user.has_group('tsc_control_cash_payments.tsc_make_cash_payment_group'):
            options = "[('company_id', '=', company_id),('type', 'in', ('bank', 'cash'))]"
        else:
            options = "[('company_id', '=', company_id),('type', '=', 'bank')]"

        return options

    journal_id = fields.Many2one('account.journal', store=True, readonly=False,
        compute='_compute_journal_id',
        domain=tsc_journal_domain,)

class TSCAccountPayment(models.Model):
    _inherit = 'account.payment'

    tsc_check_user_group = fields.Boolean(
        string="Revisa el grupo del usuario activo",
        compute="_compute_tsc_check_user_group",
        store=False
    )

    @api.depends('state')
    def _compute_tsc_check_user_group(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])

        if res_user.has_group('tsc_control_cash_payments.tsc_make_cash_payment_group'):
            self.tsc_check_user_group = True
        else:
            self.tsc_check_user_group = False

    @api.model_create_multi
    def create(self, vals_list):
        # OVERRIDE
        write_off_line_vals_list = []

        for vals in vals_list:

            # Hack to add a custom write-off line.
            write_off_line_vals_list.append(vals.pop('write_off_line_vals', None))

            # Force the move_type to avoid inconsistency with residual 'default_move_type' inside the context.
            vals['move_type'] = 'entry'

            # Force the computation of 'journal_id' since this field is set on account.move but must have the
            # bank/cash type.
            if 'journal_id' not in vals:
                vals['journal_id'] = self._get_default_journal().id

            search_journal = self.env['account.journal'].search([('id', '=', vals['journal_id'])])
            if search_journal and search_journal.type == 'cash':
                res_user = self.env['res.users'].search([('id', '=', self._uid)])

                if res_user.has_group('tsc_control_cash_payments.tsc_make_cash_payment_group'):
                    continue
                else:
                    raise UserError(_("You are not authorized to record cash payments."))
            # Since 'currency_id' is a computed editable field, it will be computed later.
            # Prevent the account.move to call the _get_default_currency method that could raise
            # the 'Please define an accounting miscellaneous journal in your company' error.
            if 'currency_id' not in vals:
                journal = self.env['account.journal'].browse(vals['journal_id'])
                vals['currency_id'] = journal.currency_id.id or journal.company_id.currency_id.id

        payments = super().create(vals_list)

        for i, pay in enumerate(payments):
            write_off_line_vals = write_off_line_vals_list[i]

            # Write payment_id on the journal entry plus the fields being stored in both models but having the same
            # name, e.g. partner_bank_id. The ORM is currently not able to perform such synchronization and make things
            # more difficult by creating related fields on the fly to handle the _inherits.
            # Then, when partner_bank_id is in vals, the key is consumed by account.payment but is never written on
            # account.move.
            to_write = {'payment_id': pay.id}
            for k, v in vals_list[i].items():
                if k in self._fields and self._fields[k].store and k in pay.move_id._fields and pay.move_id._fields[k].store:
                    to_write[k] = v

            if 'line_ids' not in vals_list[i]:
                to_write['line_ids'] = [(0, 0, line_vals) for line_vals in pay._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals)]

            pay.move_id.write(to_write)

        return payments

class TSCAccountJournal(models.Model):
    _inherit = 'account.journal'

    tsc_check_user_group = fields.Boolean(
        string="Revisa el grupo del usuario activo",
        compute="_compute_tsc_check_user_group",
        store=False
    )

    @api.model
    def _compute_tsc_check_user_group(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])

        for jounal in self:
            if res_user.has_group('tsc_control_cash_payments.tsc_make_cash_payment_group'):
                jounal.tsc_check_user_group = True
            else:
                jounal.tsc_check_user_group = False