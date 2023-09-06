# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase

class tsc_PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.model
    def _get_picking_type(self, company_id):
        tsc_user_in_internal_group = self.env.user.has_group('tsc_adjustments_for_internal_purchases.tsc_internal_purchases_group')
        tsc_user_in_merchandise_group = self.env.user.has_group('tsc_adjustments_for_internal_purchases.tsc_merchandise_purchase_group')
        
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id)])
        if not picking_type:
            picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming'), ('warehouse_id', '=', False)])

        if tsc_user_in_internal_group and not tsc_user_in_merchandise_group:
            picking_type = picking_type.search([('tsc_picking_internal_use', '=', True)])

        if tsc_user_in_merchandise_group and not tsc_user_in_internal_group:
            picking_type = picking_type.search([('tsc_picking_internal_use', '=', False)])
            
        return picking_type[:1]

   

    
    

 







                
        

