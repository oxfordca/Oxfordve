# -*- coding: utf-8 -*-
from odoo import api, fields, models

class TscProductTemplate(models.Model):
    _inherit = "product.template"

    tsc_categ_id_internal_purpose = fields.Boolean(
        related="categ_id.tsc_internal_purpose_category", 
        string="Is the product's category for internal use?"
    )

    tsc_quantity_warehouse_internal_assignment = fields.Float(
        default=0.0, 
        compute="tsc_compute_warehouse_internal_assignment"
    )
    tsc_warehouse_internal_pending_assignment = fields.Float(
        default=0.0, 
        compute="tsc_compute_warehouse_internal_assignment"
    )

    @api.depends(
        'product_variant_ids.qty_available',
        'product_variant_ids.virtual_available',
        'product_variant_ids.incoming_qty',
        'product_variant_ids.outgoing_qty',
    )
    def tsc_compute_warehouse_internal_assignment(self):
        for record in self:
            tsc_in_warehouses = self.env['stock.quant'].search([
                    ('product_id', '=', record.id), 
                    ('location_id.tsc_location_internal_assignment', '=', True)
            ])
            record.tsc_quantity_warehouse_internal_assignment = sum(
                [tsc_in_warehouse.quantity for tsc_in_warehouse in tsc_in_warehouses]
            ) 
            record.tsc_warehouse_internal_pending_assignment = (
                record.qty_available - record.tsc_quantity_warehouse_internal_assignment
            )


class TscProductProduct(models.Model):
    _inherit = "product.product"

    tsc_warehouse_internal_assignment = fields.Float(
        default=0.0, 
        compute="tsc_compute_warehouse_internal_assignment"
    )

    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state')
    @api.depends_context(
        'lot_id', 'owner_id', 'package_id', 'from_date', 'to_date',
        'location', 'warehouse',
    )
    def tsc_compute_warehouse_internal_assignment(self):
        for record in self:
            tsc_in_warehouses = self.env['stock.quant'].search([
                    ('product_id', '=', record.id), 
                    ('location_id.tsc_location_internal_assignment', '=', True)
            ])
            record.tsc_quantity_warehouse_internal_assignment = sum(
                [tsc_in_warehouse.quantity for tsc_in_warehouse in tsc_in_warehouses]
            ) 
            record.tsc_warehouse_internal_pending_assignment = (
                record.qty_available - record.tsc_quantity_warehouse_internal_assignment
            )
        
    