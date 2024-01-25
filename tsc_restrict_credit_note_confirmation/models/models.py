# -*- coding: utf-8 -*-

from odoo import _, api, exceptions, fields, models, _
from odoo.exceptions import UserError

class TSCAccountMove(models.Model):
    _inherit = 'account.move'

    tsc_check_user_group = fields.Boolean(
        string="Revisa el grupo del usuario activo",
        compute="_compute_tsc_check_user_group",
        store=False
    )

    @api.model_create_multi
    def create(self, vals_list):

        res = super(TSCAccountMove, self).create(vals_list)
        
        tsc_has_group = self.env.user.has_group(
            'tsc_restrict_credit_note_confirmation.tsc_group_create_customer_corrective_invoices'
        )
        if res.move_type == 'out_refund' and not tsc_has_group:
            raise UserError(_('Due to security restrictions, you have no permission to validate this operation.'))        
            
        return res

    @api.depends('state')
    def _compute_tsc_check_user_group(self):
        self.tsc_check_user_group = False
        if self.move_type == 'out_refund':
            res_user = self.env['res.users'].search([('id', '=', self._uid)])

            if res_user.has_group('tsc_restrict_credit_note_confirmation.tsc_confirm_customer_credit_note_group'):
                if ((self.state != 'draft') or (self.auto_post == True) or (self.move_type == 'entry') or (self.display_inactive_currency_warning == True)):
                    self.tsc_check_user_group = True
                else:
                    self.tsc_check_user_group = False
            else:
                self.tsc_check_user_group = True
        else:
            if ((self.state != 'draft') or (self.auto_post == True) or (self.move_type == 'entry') or (self.display_inactive_currency_warning == True)):
                self.tsc_check_user_group = True


class TSCAccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    @api.model
    def _tsc_get_selection(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])

        if res_user.has_group('tsc_restrict_credit_note_confirmation.tsc_confirm_customer_credit_note_group'):
            if self._context.get('lang', 'en_EN') == 'es_ES':
                options = [
                    ('refund', 'Reembolso parcial'),
                    ('cancel', 'Reembolso completo'),
                    ('modify', 'Reembolso completo y nuevo borrador de factura')
                ]
            else:
                options = [
                    ('refund', 'Partial Refund'),
                    ('cancel', 'Full Refund'),
                    ('modify', 'Full refund and new draft invoice')
                ]
        else:
            if self._context.get('lang', 'en_EN') == 'es_ES':
                options = [
                    ('refund', 'Reembolso parcial'),
                ]
            else:
                options = [
                    ('refund', 'Partial Refund'),
                ]

        return options

    refund_method = fields.Selection(
        selection=_tsc_get_selection,
        string='Credit Method',
        required=True,
        help='Choose how you want to credit this invoice. You cannot "modify" nor "cancel" if the invoice is already reconciled.',
        translate=True
    )