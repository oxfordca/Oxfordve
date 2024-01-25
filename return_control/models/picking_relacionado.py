# -*- coding: utf-8 -*-

from odoo import models, api, fields
from odoo.exceptions import UserError

class StockPickingRelacionado(models.Model):
    
    _inherit = 'stock.picking'
    
    nota_cred = fields.Char(string="Nota de Crédito", readonly=True)
    uso_locacion = fields.Selection(related="location_id.usage")
    es_devolucion = fields.Boolean(string="¿Es una devolución?", compute='compute_devolucion', store=True)
    
    @api.depends('picking_type_code', 'uso_locacion')
    def compute_devolucion(self):
        for pick in self:
            condiciones = pick.picking_type_code == 'incoming' and pick.uso_locacion == 'customer'
            pick.es_devolucion = condiciones

    def button_validate(self):
        tsc_has_group = self.env.user.has_group(
            'return_control.group_validar_devoluciones'
        )

        for record in self:
            if (
                (record.picking_type_code == 'incoming' and record.uso_locacion == 'customer') and
                not tsc_has_group
            ):
                raise UserError('Por restricciones de seguridad, no tiene permiso para validar esta operación.')

        return super(StockPickingRelacionado, self).button_validate()
  
               

    
    

  
    