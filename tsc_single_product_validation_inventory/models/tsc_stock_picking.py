# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class TscStockPicking(models.Model):

    _inherit = 'stock.picking'

    tsc_message = fields.Char(string="Temporal Message")

    def write(self, values):
        tsc_res = super().write(values)

        if self.picking_type_code == "internal":
            tsc_products = [
                (tsc_product.id, tsc_product.display_name) for tsc_move in self.move_lines for tsc_product in tsc_move.product_id
            ]
            tsc_products_unique = set()
            tsc_duplicates = [
                tsc_product for tsc_product in tsc_products 
                if tsc_product in tsc_products_unique or (tsc_products_unique.add(tsc_product) or False)
            ]
    
            tsc_final_message = ""
            if len(tsc_duplicates) > 0:
                tsc_products_names = {
                    duplicate[1]
                    for duplicate in tsc_duplicates 
                }     
                tsc_message_preffix = _("The following product(s) are repeated in this inventory operation: ")
                tsc_message_suffix = ', '.join(tsc_products_names) + "."
                tsc_final_message = tsc_message_preffix + tsc_message_suffix
                
            if self.tsc_message != tsc_final_message:
                self.tsc_message = tsc_final_message

        
        return tsc_res

