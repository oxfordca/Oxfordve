# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AMRExtension(models.TransientModel):
    
    _inherit = 'account.move.reversal'
        
    dev_mercancia = fields.Boolean(string="Devolución de Mercancía", 
                                   compute="tsc_compute_dev_mercancia",
                                  readonly=False)
    origen_invoice = fields.Char(related="move_ids.invoice_origin")
    stock_pick = fields.Many2one(comodel_name="stock.picking", 
                                 string="Albarán Asociado")

    @api.depends('move_type')
    def tsc_compute_dev_mercancia(self):
        for record in self:
            record.dev_mercancia = record.move_type == "out_invoice"  

    @api.onchange('dev_mercancia')
    def empty_sp(self):
        if not self.dev_mercancia:
            self.stock_pick = False
    
    def _prepare_default_reversal(self, move):
        res = super(AMRExtension, self)._prepare_default_reversal(move)
        res.update([('dev_mercancia', self.dev_mercancia), ('stock_pick', self.stock_pick.id)])
        return res 
    

        

        
        