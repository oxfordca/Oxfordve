# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class tsc_stock_picking(models.Model):
    _inherit = 'stock.picking'

    tsc_control_number_free_form = fields.Char(
        string='Control number free form',
        help='To have control, indicate the free form number used when printing this transfer',
        required=False,
        readonly=False,
        store=True,
        copy=True,
        tracking=True
    )

    tsc_control_number_manual = fields.Char(
        string='Control number manual',
        help='Control number for printing Dispatch Notes on letterhead. This number will be reflected on the print',
        required=False,
        readonly=False,
        store=True,
        copy=True,
    )

    tsc_control_number_formated = fields.Char(
        string='Control number manual',
        help='Control number for printing Dispatch Notes on letterhead. This number will be reflected on the print',
        required=False,
        readonly=False,
        store=True,
        copy=True,
        tracking=True
    )

    tsc_reason_transfer = fields.Text(
        string='Reason for transfer',
        help='Optional information for Dispatch Notes, about the reason for the transfer',
        required=False,
        readonly=False,
        store=True,
        copy=True,
        tracking=True
    )

    tsc_currency_dispatch_note = fields.Many2one(
        'res.currency', 
        string='Currency',
        help='Currency in which the total of the merchandise included in the Dispatch Note will be expressed',
        required=False,
        readonly=False, 
        store=True,
        copy=True,
        tracking=True,
        default=False
    )

    tsc_exchange_rate_dispatche_note = fields.Float(
        string='Exchange rate',
        help='Exchange rate according to the effective date of the Dispatch Note',
        required=False,
        readonly=True,
        store=True,
        copy=False
    )

    @api.constrains('tsc_control_number_manual')
    def _tsc_check_control_number_manual(self):
        for record in self:
            if record.tsc_control_number_manual:
                if not record.tsc_control_number_manual.isdigit():
                    raise ValidationError(_('Manual control number only accepts numbers'))
                
                if len(record.tsc_control_number_manual) > 6:
                    raise ValidationError(_('Manual control number can only contain up to 6 numbers'))

                branch_abbrv = record.branch_id.abbrv if record.branch_id else False
                if not branch_abbrv:
                    raise ValidationError(_('The branch abbreviation for generating the control number has not been defined'))
                
                record.tsc_control_number_formated = f"{branch_abbrv}-{record.tsc_control_number_manual.zfill(6)}"

    @api.constrains('state', 'tsc_currency_dispatch_note', 'date_done')
    def _check_exchange_rate_on_done_state(self):
        for record in self:
            if record.state == 'done' and record.tsc_currency_dispatch_note and record.date_done:
                for rate in record.tsc_currency_dispatch_note.rate_ids:
                    rate_date = datetime.combine(rate.name, datetime.min.time())
                    if rate_date <= record.date_done:
                        record.tsc_exchange_rate_dispatche_note = rate.company_rate
                        break
            else:
                record.tsc_exchange_rate_dispatche_note = 0.0
