from odoo import fields, models, api


class SetVehiclesWizard(models.TransientModel):
    _name = 'set.vehicles.wizard'
    _description = 'Set Vehicles Wizard'

    move_id = fields.Many2one('account.move')
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle')

    def action_confirm(self):
        self.ensure_one()
        if self.move_id:
            for line in self.move_id.invoice_line_ids:
                line.fleet_vehicle_ids = line.fleet_vehicle_ids | self.vehicle_id