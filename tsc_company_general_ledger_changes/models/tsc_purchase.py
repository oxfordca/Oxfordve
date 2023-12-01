# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    tsc_is_transit = fields.Boolean(string='Products in transit?', 
                                    help="Determines whether the products on this purchase order are in transit from the supplier's location",
                                    required=False,
                                    readonly=False,
                                    store=True,
                                    copied=True,
                                    tracking=True,
                                    default=False,
                                    compute="_tsc_compute_is_transit")

    @api.constrains('tsc_is_transit')
    def _check_tsc_is_transit(self):
        for record in self:
            if record.is_shipped and record.tsc_is_transit:
                raise ValidationError(_('The products have already been received'))


    @api.depends('picking_ids', 'picking_ids.state')
    def _tsc_compute_is_transit(self):
        for order in self:
            if order.picking_ids and all(x.state in ['done', 'cancel'] for x in order.picking_ids):
                order.tsc_is_transit = False
