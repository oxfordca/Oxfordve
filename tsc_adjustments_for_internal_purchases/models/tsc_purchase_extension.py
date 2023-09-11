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
            picking_type = picking_type.search([('tsc_picking_merchandise_use', '=', True)])
            
        return picking_type[:1]

    @api.model_create_multi
    def create(self, vals_list):
        self.tsc_check_values(vals_list[0])     
        return super(tsc_PurchaseOrder, self).create(vals_list)

    def write(self, vals):
        self.tsc_check_values(vals)
        return super(tsc_PurchaseOrder, self).write(vals)

    def tsc_check_groups(self, tsc_picking_type_id, first_group, second_group, property):       
        if first_group and not second_group:
            if tsc_picking_type_id and not tsc_picking_type_id[property]:
                raise UserError("No tiene permiso para operaciones de recepción de este tipo. Por favor compruebe su perfil como usuario de Compras.")

    def tsc_check_values(self, vals):
        tsc_user_in_internal_group = self.env.user.has_group('tsc_adjustments_for_internal_purchases.tsc_internal_purchases_group')
        tsc_user_in_merchandise_group = self.env.user.has_group('tsc_adjustments_for_internal_purchases.tsc_merchandise_purchase_group')

        if 'picking_type_id' in vals:
            tsc_picking_type_id = self.env['stock.picking.type'].browse(vals.get('picking_type_id'))
            self.tsc_check_groups(tsc_picking_type_id, tsc_user_in_internal_group, tsc_user_in_merchandise_group, "tsc_picking_internal_use")
            self.tsc_check_groups(tsc_picking_type_id, tsc_user_in_merchandise_group, tsc_user_in_internal_group, "tsc_picking_merchandise_use")
  
                

    
    

 







                
        

