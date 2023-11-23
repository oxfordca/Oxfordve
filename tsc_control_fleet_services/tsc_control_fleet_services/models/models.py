# -*- coding: utf-8 -*-

from odoo import _, api, exceptions, fields, models


class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    state = fields.Selection(
        [
            ('new', 'New'),
            ('running', 'Running'),
            ('done', 'Done'),
            ('confirm', 'Confirm'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
        string='Stage',
        group_expand='_expand_states',
        tracking=True
    )

    tsc_budget_number = fields.Char(
        string="Budget number",
        help="Budget number",
        required=True,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        translate=True
    )

    @api.onchange('state')
    def _onchange_state(self):
        # Verificar si el servicio existe para confirmar
        service_exists = self.env['fleet.vehicle.log.services'].search([('id', '=', self._origin.id)])

        # Verificar si el usuario pertenece al grupo específico para confirmar un servicio
        if 'Confirm services' not in self.env.user.groups_id.mapped('name') and self.state == 'confirm' and service_exists:
            # Si el usuario no pertenece al grupo, lanzar una excepción
            raise exceptions.UserError('Usuario no autorizado para confirmar un servicio.')
        
        if 'Cancel services' not in self.env.user.groups_id.mapped('name') and self.state == 'cancelled' and service_exists:
            # Si el usuario no pertenece al grupo, lanzar una excepción
            raise exceptions.UserError('Usuario no autorizado para cancelar un servicio.')
        
        if self.state == 'confirm' and not service_exists and 'Confirm services' not in self.env.user.groups_id.mapped('name'):
            self.state = 'new'
            return {'warning': {'title': 'Advertencia', 'message': 'Usuario no autorizado para crear un servicio confirmado. El servicio se creará con estado Nuevo'}}

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    tsc_truck_number = fields.Char(
        string="Truck number",
        help="Truck number",
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        translate=True
    )

    tsc_drivers_license = fields.Char(
        string="Driver's license",
        related='driver_id.tsc_drivers_license',
        store=False,
        readonly=True
    )

    tsc_license_degree = fields.Selection(
        string="License Degree",
        related='driver_id.tsc_license_degree',
        store=False,
        readonly=True
    )

    tsc_last_air_filter_change = fields.Date(
        string='Last air filter change',
        help='Last air filter change',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True
    )

    tsc_last_fuel_filter_change = fields.Date(
        string='Last fuel filter change',
        help='Last fuel filter change',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True
    )

    tsc_last_tire_change = fields.Date(
        string='Last tire change',
        help='Last tire change',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True
    )

    tsc_type_rubber = fields.Char(
        string='Type rubber',
        help='Type rubber',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        translate=True
    )

    tsc_last_battery_change = fields.Date(
        string='Last battery change',
        help='Last battery change',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True
    )

    tsc_type_battery = fields.Char(
        string='Type battery',
        help='Type battery',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        translate=True
    )

    tsc_battery_serial = fields.Char(
        string='Battery serial',
        help='Battery serial',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        translate=True
    )

    tsc_last_brake_check = fields.Date(
        string='Last brake check',
        help='Last brake check',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True
    )

    tsc_last_gasket_change = fields.Date(
        string='Last gasket change',
        help='Last gasket change',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True
    )

    tsc_safety_kit = fields.Boolean(
        string='Do you have a safety kit (first aid)?',
        help='Do you have a safety kit (first aid)?',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

    tsc_safe_deposit_box = fields.Boolean(
        string='Do you have a safe?',
        help='Do you have a safe?',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

    tsc_cross_key = fields.Boolean(
        string='Do you have a cross key?',
        help='Do you have a cross key?',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

    tsc_emergency_triangle = fields.Boolean(
        string='Do you have an emergency triangle?',
        help='Do you have an emergency triangle?',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

    tsc_fire_extinguisher = fields.Boolean(
        string='Do you have a fire extinguisher?',
        help='Do you have a fire extinguisher?',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

    tsc_hydraulic_jack = fields.Boolean(
        string='Do you have a hydraulics jack?',
        help='Do you have a hydraulics jack?',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

    tsc_spare_rubber = fields.Boolean(
        string='Do you have spare rubber?',
        help='Do you have spare rubber?',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

    tsc_gps = fields.Boolean(
        string='Do you have a GPS?',
        help='Do you have a GPS?',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

    tsc_fuel_cap = fields.Boolean(
        string='Do you have a fuel cap?',
        help='Do you have a fuel cap?',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

    tsc_date_purchase = fields.Date(
        string='Date of purchase',
        help='Date of purchase',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True
    )

    tsc_initial_mileage = fields.Char(
        string='Initial mileage',
        help='Mileage at time of purchase',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        translate=True
    )

    tsc_payment_registration_date = fields.Date(
        string='Payment registration date',
        help='Payment registration date',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True
    )

    tsc_sale_notary = fields.Boolean(
        string='Sale by notary',
        help='Sale by notary',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

    tsc_direct_title = fields.Boolean(
        string='Direct title',
        help='Direct title',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

    tsc_assured = fields.Boolean(
        string='Assured',
        help='Assured',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

    tsc_permission = fields.Boolean(
        string='Permission',
        help='Permission',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

    tsc_rupdae = fields.Boolean(
        string='RUPDAE',
        help='Single Registry of People Who Develop Economic Activities',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

    tsc_racda = fields.Boolean(
        string='RACDA',
        help='Registry of Activities Capable of Degrading the Environment',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

    tsc_rotc = fields.Boolean(
        string='ROTC',
        help='Registry of Freight Transport Operators',
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        default=False
    )

class Partner(models.Model):
    _inherit = "res.partner"

    tsc_drivers_license = fields.Char(
        string="Driver's license",
        help="Driver's license number",
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        translate=True
    )

    tsc_license_degree = fields.Selection(
        [
            ('1A', '1st grade - Type A'),
            ('1B', '1st grade - Type B'),
            ('2A', '2nd grade - Type A'),
            ('2B', '2nd grade - Type B'),
            ('3G', '3rd grade'),
            ('4G', '4th grade'),
            ('5G', '5th grade'),
            ('TSP', 'Higher professional degree - HPD'),
        ],
        string='License Degree',
        help="Driver's license degree",
        required=False,
        readonly=False,
        store=True,
        copy=False,
        tracking=True,
        translate=True
    )