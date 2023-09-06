# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import UserError

class tsc_StockLocation(models.Model):

    _name = 'stock.location'
    _inherit = ['stock.location', 'mail.thread']
    
    tsc_location_internal_use = fields.Boolean(string="Is it for Internal Purchases?", 
                                              help="Mark as checked if the location will be used exclusively for internal purchase products.",
                                              required=False,
                                              readonly=False,
                                              store=True,
                                              copy=False,
                                              tracking=False,
                                              default=False)


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
    @api.model
    def create(self, vals):
        if vals.get('tsc_picking_internal_use'):
            tsc_src_location = self.env['stock.location'].browse(vals.get('default_location_src_id'))
            tsc_dest_location = self.env['stock.location'].browse(vals.get('default_location_dest_id'))
            if not tsc_src_location.tsc_location_internal_use and not tsc_dest_location.tsc_location_internal_use:
                raise UserError('Para que la operación sea empleada para Compras Internas, la ubicación origen o la ubicación destino también debe ser para Compras Internas. Por favor, compruebe la configuración de las ubicaciones.')
        
        return super(tsc_StockPickingType, self).create(vals)

    def write(self, vals):

        for picking_type in self:
           
            if ('tsc_picking_internal_use' in vals and vals.get('tsc_picking_internal_use') == True)\
            or picking_type.tsc_picking_internal_use:
                
                tsc_location_src_location = picking_type.default_location_src_id
                tsc_location_dest_location = picking_type.default_location_dest_id

                if vals.get('default_location_src_id'):
                    tsc_id = vals.get('default_location_src_id')
                    tsc_location_src_location = self.env['stock.location'].browse(tsc_id)

                if vals.get('default_location_dest_id'):
                    tsc_id = vals.get('default_location_dest_id')
                    tsc_location_dest_location = self.env['stock.location'].browse(tsc_id)


                if not tsc_location_src_location.tsc_location_internal_use and not tsc_location_dest_location.tsc_location_internal_use:
                    raise UserError('Para que la operación sea empleada para Compras Internas, la ubicación origen o la ubicación destino también debe ser para Compras Internas. Por favor, compruebe la configuración de las ubicaciones.')
            

                    
        
        return super(tsc_StockPickingType, self).write(vals)




