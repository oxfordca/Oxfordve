from odoo import fields, models, api


class ImportSummary(models.Model):
    _name = 'import.summary'
    _description = 'Import Summary'

    move_id = fields.Many2one('account.move', string='Related Invoice', required=True)
    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order', compute='_compute_purchase_order_id', store=True)
    name = fields.Char(string='Number', related='move_id.name', store=True)
    invoice_date = fields.Date(string='Invoice Date', related='move_id.invoice_date', store=True)
    invoice_state = fields.Selection(string='Invoice State', related='move_id.state')
    invoice_payment_state = fields.Selection(string='Invoice Payment State', related='move_id.payment_state')
    invoice_branch_id = fields.Many2one(string='Branch', related='move_id.branch_id', store=True)
    invoice_currency_id = fields.Many2one(string='Currency', related='move_id.currency_id')
    invoice_amount_total = fields.Monetary(string='Total', related='move_id.amount_total', currency_field='invoice_currency_id')
    invoice_amount_residual = fields.Monetary(string='Amount Due', related='move_id.amount_residual', currency_field='invoice_currency_id')
    invoice_partner_id = fields.Many2one(string='Partner', related='move_id.partner_id', store=True)
    purchase_order_is_shipped = fields.Boolean(string='Products received', related='purchase_order_id.is_shipped', store=True)
    purchase_order_is_transit = fields.Boolean(string='Products in transit', related='purchase_order_id.tsc_is_transit', store=True)
    purchase_order_date_planned = fields.Datetime(string='Receipt Date', related='purchase_order_id.date_planned', store=True)
    claim = fields.Boolean(string='Claim')
    payment_and_doc = fields.Boolean(string='Payment and Doc')
    no_payment_no_doc = fields.Boolean(string="No Payment and No Doc")
    bl_number = fields.Char(string='BL Number')
    container_number = fields.Char(string='Container Number')
    description = fields.Text(string='Description')
    information = fields.Text(string='Information')
    arrival_date = fields.Date(string='Arrival Date')
    claim_date = fields.Date(string='Claim Date')
    shipping_line = fields.Char(string='Shipping Line')
    days_off = fields.Integer(string='Days Off')
    row_color = fields.Char(compute='_compute_row_color', store=True)

    def create_import_summary(self, account_move):
        if account_move.importation_check:
            existing_summary = self.search([('move_id', '=', account_move.id)], limit=1)
            if not existing_summary:
                self.create({
                    'move_id': account_move.id,
                    'bl_number': '',
                    'container_number': '',
                    'description': '',
                    'arrival_date': False,
                    'claim_date': False,
                    'shipping_line': '',
                    'days_off': 0,
                })

    def delete_import_summary(self, account_move):
        if not account_move.importation_check:
            summary = self.search([('move_id', '=', account_move.id)], limit=1)
            if summary:
                summary.unlink()

    def _check_if_receiving_completed(self, move_id):
        purchase_order = move_id.invoice_origin and self.env['purchase.order'].search(
            [('name', '=', move_id.invoice_origin)], limit=1)

        if purchase_order:
            pickings = purchase_order.picking_ids

            valid_pickings = [picking for picking in pickings if picking.state != 'cancel']
            if not valid_pickings:
                return False

            return all(picking.state == 'done' for picking in valid_pickings)
        return False

    def _check_if_receiving_pending(self, move_id):
        purchase_order = move_id.invoice_origin and self.env['purchase.order'].search(
            [('name', '=', move_id.invoice_origin)], limit=1)

        if purchase_order:
            pickings = purchase_order.picking_ids

            pending_pickings = [picking for picking in pickings if picking.state not in ('done', 'cancel')]
            done_pickings = [picking for picking in pickings if picking.state == 'done']

            # Returns True only if there is at least one 'done' and at least one pending.
            return bool(pending_pickings) and bool(done_pickings)
        return False

    @api.depends('move_id', 'payment_and_doc', 'no_payment_no_doc', 'invoice_payment_state',
                 'purchase_order_id.picking_ids.state')
    def _compute_row_color(self):
        for record in self:
            if self._check_if_receiving_completed(record.move_id):
                record.row_color = 'blue'
            elif self._check_if_receiving_pending(record.move_id):
                record.row_color = 'red'
            elif record.payment_and_doc:
                record.row_color = 'black'
            elif record.invoice_payment_state == 'paid':
                record.row_color = 'yellow'
            elif record.no_payment_no_doc:
                record.row_color = 'orange'
            else:
                record.row_color = 'green'

    @api.depends('move_id', 'move_id.invoice_origin')
    def _compute_purchase_order_id(self):
        for record in self:
            purchase_order = self.env['purchase.order'].search([('name', '=', record.move_id.invoice_origin)], limit=1)
            record.purchase_order_id = purchase_order.id if purchase_order else False
