# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import UserError

class tsc_ProductTemplate(models.Model):

    _inherit = 'product.template'

    #@tools.ormcache()
    def _get_default_category_id(self):
        if self.env.user.has_group('tsc_adjustments_for_internal_purchases.tsc_internal_purchases_group'):
            tsc_find_category = self.env['product.category'].search([('tsc_internal_purpose_category', '=', True)])
            return tsc_find_category[:1]
        return self.env.ref('product.product_category_all')

    @api.model
    def tsc_get_categories(self):
        if self.env.user.has_group('tsc_adjustments_for_internal_purchases.tsc_internal_purchases_group'):
            return ['|', ('tsc_internal_purpose_category', '=', True), ('parent_id.tsc_internal_purpose_category','=',True)]
        return []
        
    
    categ_id = fields.Many2one(
        'product.category', 'Product Category',
        change_default=True, domain=tsc_get_categories, default=_get_default_category_id, group_expand='_read_group_categ_id', required=True, help="Select category for the current product")

class tsc_ProductCategory(models.Model):

    _inherit = 'product.category'

    tsc_internal_purpose_category = fields.Boolean(string="Is it for internal use?", default=False)
    
