from odoo import fields, models, api


class FleetVehicleLogServicesInherit(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    move_id = fields.Many2one('account.move', string='Invoice', copy=False)