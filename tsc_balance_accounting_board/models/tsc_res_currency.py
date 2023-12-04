# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class tsc_ResCurrency(models.Model):

    _inherit = 'res.currency'

    tsc_stable_rate = fields.Boolean(string="Stable Currency",
                                              help="Identifies if the currency is the main unchangable currency.",
                                              store=True,
                                              default=False)

    @api.onchange('tsc_stable_rate')
    def tsc_onchange_tsc_stable_rate(self):
        tsc_find_stable_currency = self.env['res.currency'].search([('tsc_stable_rate','=',True)], limit=1)
        for record in self:
            if tsc_find_stable_currency and tsc_find_stable_currency.id != record._origin.id and record.tsc_stable_rate:
                raise UserError(_('An stable currency was already choosen. Current stable currency name: %s') % tsc_find_stable_currency.name)