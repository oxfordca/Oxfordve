from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    box_cero = fields.Monetary(string='Box cero')
    box_uno = fields.Monetary(string='Box uno')
    box_dos = fields.Monetary(string='Box dos')