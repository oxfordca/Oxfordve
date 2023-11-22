# -*- coding: utf-8 -*-

from odoo import _, api, exceptions, fields, models


class CommissionForCategory(models.Model):
    _name = 'commission.for.category'
    _description = 'Commission for category'
    _inherit = 'commission.commission'

    categ_id = fields.Many2one(
        'product.category',
        string="Categoría",
        required=True,
    )
    basado_en = fields.Many2one(
        comodel_name='commission.for.category',
        domain="[('id', '!=', id), ('categ_id', '=', categ_id)]"
    )

    _sql_constraints = [
        (
            'unique_categ_id_and_commission_id',
            'UNIQUE(categ_id, id)',
            'La categoria tiene una o más comisiones repetidas. Por favor, verifique'
        ),
    ]
