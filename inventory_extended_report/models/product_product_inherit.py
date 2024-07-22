from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.product"

    box_cero = fields.Monetary(string='Box cero', compute='_compute_boxes')
    box_uno = fields.Monetary(string='Box uno', compute='_compute_boxes')
    box_dos = fields.Monetary(string='Box dos', compute='_compute_boxes')

    valorizado_box_cero = fields.Float(string='Valorizado Box Cero', compute='_compute_valorizados')
    valorizado_box_uno = fields.Float(string='Valorizado Box Uno', compute='_compute_valorizados')
    valorizado_box_dos = fields.Float(string='Valorizado Box Dos', compute='_compute_valorizados')

    qty_available_non_consign = fields.Float(
        string='Cantidad a mano (Sin consignación)',
        compute='_compute_qty_available_non_consign',
        help="Cantidad actual de los productos excluyendo los almacenes a consignación."
    )

    @api.depends('product_tmpl_id.box_cero', 'product_tmpl_id.box_uno', 'product_tmpl_id.box_dos')
    def _compute_boxes(self):
        for record in self:
            record.box_cero = record.product_tmpl_id.box_cero
            record.box_uno = record.product_tmpl_id.box_uno
            record.box_dos = record.product_tmpl_id.box_dos

    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state')
    @api.depends_context(
        'lot_id', 'owner_id', 'package_id', 'from_date', 'to_date',
        'location', 'warehouse', 'allowed_company_ids'
    )
    def _compute_qty_available_non_consign(self):
        products = self.filtered(lambda p: p.type != 'service')
        warehouse_ids = self.env['stock.warehouse'].search([('consignment_inventory', '=', False)]).ids

        quantities = products.with_context(warehouse=warehouse_ids)._compute_quantities_dict(
            self._context.get('lot_id'),
            self._context.get('owner_id'),
            self._context.get('package_id'),
            self._context.get('from_date'),
            self._context.get('to_date')
        )

        for product in products:
            product.qty_available_non_consign = quantities[product.id]['qty_available']

        services = self - products
        services.qty_available_non_consign = 0.0

    @api.depends('box_cero', 'box_uno', 'box_dos')
    def _compute_valorizados(self):
        for record in self:
            box_cero = record.box_cero if record.box_cero else 0.0
            box_uno = record.box_uno if record.box_uno else 0.0
            box_dos = record.box_dos if record.box_dos else 0.0

            record.valorizado_box_cero = box_cero * record.qty_available_non_consign
            record.valorizado_box_uno = box_uno * record.qty_available_non_consign
            record.valorizado_box_dos = box_dos * record.qty_available_non_consign