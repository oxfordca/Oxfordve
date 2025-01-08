from odoo import fields, models, api


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    fleet_vehicle_ids = fields.Many2many('fleet.vehicle', string='Fleet Vehicles', copy=False)
