from odoo import fields, models, api


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    amount_widget_currency_id = fields.Many2one('res.currency', string='Widget Currency', tracking=True)
    amount_widget_exchange_rate = fields.Float(string='Exchange Rate', compute='_compute_amount_widget_exchange_rate', digits=(None, 4), store=True)
    amount_widget_base_ves = fields.Float(string='Base VES', compute='_compute_amount_widget_base_ves', digits=(None, 4), store=True)
    amount_widget_tax_16 = fields.Float(string='Tax 16% $', compute='_compute_amount_widget_tax_16', digits=(None, 4), store=True)
    amount_widget_base_tax_16 = fields.Float(string='Base Tax 16%', compute='_compute_amount_widget_base_tax_16', digits=(None, 4), store=True)
    amount_widget_base_tax_16_ves = fields.Float(string='Base Tax 16% VES', compute='_compute_amount_widget_base_tax_16_ves', digits=(None, 4), store=True)
    amount_widget_base_tax_0_ves = fields.Float(string='Base Tax 0% VES', compute='_compute_amount_widget_base_tax_0_ves', digits=(None, 4), store=True)
    amount_widget_vat_ves = fields.Float(string='VAT VES', compute='_compute_amount_widget_vat_ves', digits=(None, 4), store=True)
    amount_widget_exempt_ves = fields.Float(string='Exempt VES', digits=(None, 4))
    amount_widget_total_ves = fields.Float(string='Total VES', compute='_compute_amount_widget_total_ves', digits=(None, 4), store=True)

    @api.depends('amount_widget_currency_id')
    def _compute_amount_widget_exchange_rate(self):
        for record in self:
            for x in record.amount_widget_currency_id.rate_ids:
                if record.invoice_date:
                    if x.name <= record.invoice_date:
                        record.amount_widget_exchange_rate = x.company_rate
                        break

    @api.depends('amount_untaxed', 'amount_widget_exchange_rate')
    def _compute_amount_widget_base_ves(self):
        for record in self:
            record.amount_widget_base_ves = record.amount_untaxed * record.amount_widget_exchange_rate

    @api.depends('amount_untaxed', 'amount_widget_exchange_rate')
    def _compute_amount_widget_tax_16(self):
        for record in self:
            if record.amount_widget_exchange_rate != 0:
                if record.currency_id != record.company_id.currency_id:
                    record.amount_widget_tax_16 = (record.amount_untaxed / record.amount_widget_exchange_rate) * 0.16
                else:
                    record.amount_widget_tax_16 = record.amount_untaxed * 0.16
            else:
                record.amount_widget_tax_16 = 0

    @api.depends('amount_widget_exchange_rate', 'amount_widget_tax_16')
    def _compute_amount_widget_base_tax_16(self):
        for record in self:
            record.amount_widget_base_tax_16 = record.amount_widget_tax_16 / 0.16

    @api.depends('amount_widget_base_tax_16', 'amount_widget_exchange_rate', 'amount_untaxed')
    def _compute_amount_widget_base_tax_16_ves(self):
        for record in self:
            record.amount_widget_base_tax_16_ves = record.amount_widget_base_tax_16 * record.amount_widget_exchange_rate

    @api.depends('amount_widget_base_ves', 'amount_widget_base_tax_16_ves')
    def _compute_amount_widget_base_tax_0_ves(self):
        for record in self:
            record.amount_widget_base_tax_0_ves = (record.amount_widget_base_ves - record.amount_widget_base_tax_16_ves)

    @api.depends('amount_widget_tax_16', 'amount_widget_exchange_rate')
    def _compute_amount_widget_vat_ves(self):
        for record in self:
            record.amount_widget_vat_ves = record.amount_widget_tax_16 * record.amount_widget_exchange_rate

    @api.depends('amount_total', 'amount_widget_exchange_rate', 'amount_widget_base_ves', 'amount_widget_vat_ves')
    def _compute_amount_widget_total_ves(self):
        for record in self:
            record.amount_widget_total_ves = record.amount_widget_base_ves + record.amount_widget_vat_ves
