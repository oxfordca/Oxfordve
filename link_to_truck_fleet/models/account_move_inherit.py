from odoo import fields, models, api, _
from markupsafe import Markup


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    truck_fleet_check = fields.Boolean(string='Truck Fleet')
    fleet_service_type_id = fields.Many2one('fleet.service.type', string='Service Type')

    def action_open_set_vehicles_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Assign vehicle'),
            'res_model': 'set.vehicles.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_move_id': self.id,
            }
        }

    @api.onchange('truck_fleet_check')
    def _onchange_truck_fleet_check(self):
        if not self.truck_fleet_check:
            self.fleet_service_type_id = False
            lines_to_clear = self.invoice_line_ids.filtered(lambda l: l.fleet_vehicle_ids)
            if lines_to_clear:
                lines_to_clear.write({'fleet_vehicle_ids': [(5, 0, 0)]})

                return {
                    'warning': {
                        'title': _('Vehicles Eliminated'),
                        'message': _('All assigned vehicles have been removed from the invoice lines.'),
                    }
                }

    def _get_html_link(self, record, title=None):
        """Generate the record html reference for chatter use.

        :param str title: optional reference title, the record display_name
            is used if not provided. The title/display_name will be escaped.
        :returns: generated html reference,
            in the format <a href data-oe-model="..." data-oe-id="...">title</a>
        :rtype: str
        """
        self.ensure_one()
        return Markup("<a href='#' data-oe-model='%s' data-oe-id='%s'>%s</a>") % (
            record._name, record.id, title or record.display_name
        )

    def _create_fleet_service_logs(self):
        for move in self:
            if not move.truck_fleet_check:
                continue

            lines_with_vehicles = move.invoice_line_ids.filtered(lambda l: l.fleet_vehicle_ids)
            if not lines_with_vehicles:
                continue

            existing_logs = self.env['fleet.vehicle.log.services'].search_count([('move_id', '=', move.id)])
            if existing_logs:
                continue

            budget_number = move.invoice_origin or False
            service_logs = {}
            for line in lines_with_vehicles:
                amount_per_vehicle = line.price_total / len(line.fleet_vehicle_ids)
                for vehicle in line.fleet_vehicle_ids:
                    service_logs[vehicle.id] = service_logs.get(vehicle.id, 0) + amount_per_vehicle

            if move.company_id.currency_id != move.currency_id:
                for vehicle_id, total_amount in service_logs.items():
                    service_logs[vehicle_id] = move.currency_id._convert(total_amount, move.company_id.currency_id, move.company_id, move.invoice_date)

            service_logs_data = [{
                'vehicle_id': vehicle_id,
                'vendor_id': move.partner_id.id,
                'service_type_id': move.fleet_service_type_id.id,
                'date': move.invoice_date,
                'amount': total_amount,
                'move_id': move.id,
                'tsc_budget_number': budget_number,
            } for vehicle_id, total_amount in service_logs.items()]

            if service_logs_data:
                created_logs = self.env['fleet.vehicle.log.services'].create(service_logs_data)
                log_links = [move._get_html_link(log, title=log.vehicle_id.name) for log in created_logs]
                move.message_post(body=_("Fleet service logs have been created successfully: ") + ', '.join(log_links))

    def _remove_fleet_service_logs(self):
        for move in self:
            logs = self.env['fleet.vehicle.log.services'].search([('move_id', '=', move.id)])
            if logs:
                logs.unlink()
                move.message_post(body=_("Fleet service logs have been removed."))

    def action_post(self):
        res = super(AccountMoveInherit, self).action_post()
        for record in self:
            if record.truck_fleet_check:
                record._create_fleet_service_logs()
            else:
                record._remove_fleet_service_logs()
        return res