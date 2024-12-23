from email.policy import default
from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'stock.picking'

    orden_compra= fields.Char(string="Orden de Compra" , compute='_compute_delivery_count',store=True, )
    
    @api.depends('sale_id')
    def _compute_delivery_count(self):
        for picking in self:
            if picking.sale_id:
                picking.orden_compra = str(picking.sale_id.orden_compra)
            else:
                picking.orden_compra = ''




    