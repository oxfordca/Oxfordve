# -*- coding: utf-8 -*-
from odoo import api, fields, models

class TscStockLocation(models.Model):
    _inherit = "stock.location"

    tsc_location_internal_assignment = fields.Boolean(
        string="Ubicación para asignación interna",
        help="Determina si la ubicación es empleada para registrar el movimiento de materiales y equipos asignado a personal interno.",
        required=False,
        readonly=False,
        store=True,
        default=False,
    )
    