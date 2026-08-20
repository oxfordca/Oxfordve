# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    tsc_from_confirmed_sale = fields.Boolean(
        string="From Confirmed Sale Order",
        compute="_compute_tsc_from_confirmed_sale",
        store=False,
        help="Technical field to identify if the invoice originates from a confirmed Sale Order."
    )

    tsc_is_restricted_user = fields.Boolean(
        compute="_compute_tsc_is_restricted_user",
        string="Is Restricted User"
    )

    @api.depends_context('uid')
    def _compute_tsc_is_restricted_user(self):
        has_group = self.env.user.has_group(
            'tsc_restrict_customer_invoice_edition.tsc_group_restrict_customer_invoice_edition'
        )
        for move in self:
            move.tsc_is_restricted_user = bool(has_group and move.tsc_from_confirmed_sale and move.state == 'draft')

    @api.depends('invoice_line_ids.sale_line_ids', 'invoice_line_ids.sale_line_ids.order_id.state')
    def _compute_tsc_from_confirmed_sale(self):
        for move in self:
            has_sale = False
            if move.move_type in ('out_invoice', 'out_refund'):
                sale_orders = move.invoice_line_ids.mapped('sale_line_ids.order_id')
                if any(so.state in ('sale', 'done') for so in sale_orders):
                    has_sale = True
            move.tsc_from_confirmed_sale = has_sale

    def write(self, vals):
        has_group = self.env.user.has_group(
            'tsc_restrict_customer_invoice_edition.tsc_group_restrict_customer_invoice_edition'
        )

        forbidden_header_fields = {
            'partner_id',
            'partner_shipping_id',
            'payment_reference',
            'invoice_payment_term_id',
            'journal_id',
            'currency_id',
            'branch_id',
        }

        forbidden_line_fields = {
            'product_id',
            'quantity',
            'price_unit',
            'discount',
            'product_uom_id',
            'name',
            'account_id',
        }

        if has_group:
            for rec in self:
                if rec.state == 'draft' and rec.tsc_from_confirmed_sale:
                    # 1. Validar campos prohibidos en la cabecera
                    modified_forbidden = set(vals.keys()).intersection(forbidden_header_fields)
                    if modified_forbidden:
                        raise UserError(_("Esta factura proviene de un pedido de venta confirmado. No tiene el permiso para alterar su estructura, ni contenido."))

                    # 2. Validar cambios en invoice_line_ids (Las líneas de factura que ve el usuario)
                    if 'invoice_line_ids' in vals:
                        for command in vals['invoice_line_ids']:
                            # Comando 0: Crear nueva línea -> PROHIBIDO
                            # Comando 2 o 3: Eliminar línea -> PROHIBIDO
                            # Comando 5: Borrar todas -> PROHIBIDO
                            if command[0] in (0, 2, 3, 5):
                                raise UserError(_("Esta factura proviene de un pedido de venta confirmado. No tiene el permiso para alterar su estructura, ni contenido."))

                            # Comando 1: Modificar línea existente (Aquí permitimos tax_ids y bloqueamos los prohibidos reales)
                            elif command[0] == 1 and isinstance(command[2], dict):
                                line_dict = command[2]
                                real_line_changes = {
                                    k for k, v in line_dict.items()
                                    if k in forbidden_line_fields and v is not False and v is not None
                                }
                                if real_line_changes:
                                    raise UserError(_("Esta factura proviene de un pedido de venta confirmado. No tiene el permiso para alterar su estructura, ni contenido."))

        return super(AccountMove, self).write(vals)

    def unlink(self):
        if self.env.user.has_group('tsc_restrict_customer_invoice_edition.tsc_group_restrict_customer_invoice_edition'):
            for move in self:
                if move.tsc_from_confirmed_sale and move.state == 'draft':
                    raise UserError(_("Esta factura proviene de un pedido de venta confirmado. No tiene el permiso para alterar su estructura, ni contenido."))
        return super(AccountMove, self).unlink()

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.user.has_group('tsc_restrict_customer_invoice_edition.tsc_group_restrict_customer_invoice_edition'):
            for vals in vals_list:
                move_id = vals.get('move_id')
                if move_id:
                    move = self.env['account.move'].browse(move_id)
                    
                    # Identificar si es una línea de impuestos o generada automáticamente por el motor fiscal
                    is_tax_line = (
                        vals.get('tax_line_id') or 
                        vals.get('display_type') == 'tax' or 
                        vals.get('tax_repartition_line_id') or
                        not vals.get('product_id')
                    )
                    
                    if move.tsc_from_confirmed_sale and move.state == 'draft' and not is_tax_line:
                        raise UserError(_("Esta factura proviene de un pedido de venta confirmado. No tiene el permiso para alterar su estructura, ni contenido."))
        return super(AccountMoveLine, self).create(vals_list)

    def write(self, vals):
        return super(AccountMoveLine, self).write(vals)

    def unlink(self):
        if self.env.user.has_group('tsc_restrict_customer_invoice_edition.tsc_group_restrict_customer_invoice_edition'):
            for line in self:
                if line.display_type == 'tax' or line.tax_line_id or line.tax_repartition_line_id or not line.product_id:
                    continue
                if line.move_id and line.move_id.tsc_from_confirmed_sale and line.move_id.state == 'draft':
                    raise UserError(_("Esta factura proviene de un pedido de venta confirmado. No tiene el permiso para alterar su estructura, ni contenido."))
        return super(AccountMoveLine, self).unlink()