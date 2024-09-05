# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.tools import float_round


class TscStockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def tsc_ajustar_precio_unitario(self, precio):

        for record in self:
            product_line_uom = record.move_id.product_uom
            product_storage_uom = record.product_id.uom_id

            # Verificar si las unidades de medida son distintas
            if product_line_uom != product_storage_uom:
                # Verificar si alguna de las unidades es de tipo "unidad de medida de referencia"
                if product_line_uom.uom_type == 'reference' or product_storage_uom.uom_type == 'reference':
                    # Una conversión
                    if product_line_uom.uom_type == 'reference':
                        factor_inv = product_storage_uom.factor_inv
                        uom_type = product_storage_uom.uom_type

                        if uom_type == 'bigger':
                            precio = precio / factor_inv
                        elif uom_type == 'smaller':
                            precio = precio * factor_inv

                    
                    elif product_storage_uom.uom_type == 'reference':
                        factor_inv = product_line_uom.factor_inv
                        uom_type = product_line_uom.uom_type

                        if uom_type == 'bigger':
                            precio = precio * factor_inv
                        elif uom_type == 'smaller':
                            precio = precio / factor_inv
                else:
                    # Doble conversión
                    # Convertimos el precio a la unidad de medida de almacenamiento
                    factor_inv_storage = product_storage_uom.factor_inv
                    precio = precio / factor_inv_storage if product_storage_uom.uom_type == 'bigger' else precio * factor_inv_storage

                    # Convertimos el precio a la unidad de medida de la línea de movimiento
                    factor_inv_line = product_line_uom.factor_inv
                    precio = precio / factor_inv_line if product_line_uom.uom_type == 'smaller' else precio * factor_inv_line

            return precio


class TscStockMove(models.Model):
    _inherit = 'stock.move'

    tsc_price_unit = fields.Float(string='Price', digits='Product Price', compute='_compute_tsc_price_unit')

    @api.depends('product_uom', 'product_id', 'product_id.uom_id')
    def _compute_tsc_price_unit(self):
        for record in self:
            if record.picking_id and record.picking_id.partner_id and record.product_id:
                price = list(record.picking_id.partner_id.property_product_pricelist.price_get(record.product_id.id, record.quantity_done, record.picking_id.partner_id).values())[0]
                unit_price = record.tsc_ajustar_precio_unitario(price)

                # redondeando el precio 
                price_unit_prec = self.env['decimal.precision'].precision_get('Product Price')
                rounded_price = float_round(unit_price, precision_digits=price_unit_prec)

                # precio final
                record.tsc_price_unit = rounded_price

            else:
                record.tsc_price_unit = 0.0

    def tsc_ajustar_precio_unitario(self, precio):
        for record in self:
            product_line_uom = record.product_uom
            product_storage_uom = record.product_id.uom_id

            # Verificar si las unidades de medida son distintas
            if product_line_uom != product_storage_uom:
                # Verificar si alguna de las unidades es de tipo "unidad de medida de referencia"
                if product_line_uom.uom_type == 'reference' or product_storage_uom.uom_type == 'reference':
                    # Una conversión

                    # De acuerdo a la unidad de medida de la línea de movimiento se ajusta el precio
                    if product_line_uom.uom_type == 'reference':
                        factor_inv = product_storage_uom.factor_inv
                        uom_type = product_storage_uom.uom_type

                        if uom_type == 'bigger':
                            precio = precio / factor_inv
                        elif uom_type == 'smaller':
                            precio = precio * factor_inv

                    # De acuerdo a la unidad de medida de almacenamiento se ajusta el precio
                    elif product_storage_uom.uom_type == 'reference':
                        factor_inv = product_line_uom.factor_inv
                        uom_type = product_line_uom.uom_type

                        if uom_type == 'bigger':
                            precio = precio * factor_inv
                        elif uom_type == 'smaller':
                            precio = precio / factor_inv

                else:
                    # Doble conversión
                    # Convertimos el precio a la unidad de medida de almacenamiento
                    factor_inv_storage = product_storage_uom.factor_inv
                    precio = precio / factor_inv_storage if product_storage_uom.uom_type == 'bigger' else precio * factor_inv_storage

                    # Convertimos el precio a la unidad de medida de la línea de movimiento
                    factor_inv_line = product_line_uom.factor_inv
                    precio = precio / factor_inv_line if product_line_uom.uom_type == 'smaller' else precio * factor_inv_line

            return precio

    
   

