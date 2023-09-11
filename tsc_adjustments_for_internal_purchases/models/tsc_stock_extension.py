# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class tsc_StockPickingType(models.Model):

    _name = 'stock.picking.type'
    _inherit = ['stock.picking.type', 'mail.thread']
    
    tsc_picking_internal_use = fields.Boolean(string="Is it for Internal Purchases?", 
                                              help="Mark as checked if the operation will be used exclusively for internal purchases.",
                                              required=False,
                                              readonly=False,
                                              store=True,
                                              copy=False,
                                              tracking=False,
                                              default=False)

    tsc_picking_merchandise_use = fields.Boolean(string="Is it for Merchandise Purchases?", 
                                              help="Mark as checked if the operation will be used exclusively for merchandise purchases.",
                                              required=False,
                                              readonly=False,
                                              store=True,
                                              copy=False,
                                              tracking=False,
                                              default=False)


