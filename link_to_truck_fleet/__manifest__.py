# -*- coding: utf-8 -*-
{
    'name': "Link to Truck Fleet",
    'summary': """
        Creates a new service in the fleet when a purchase invoice is made.
    """,
    'description': """
        When making a purchase invoice related to vehicle expenses, a new service record will be created in the fleet 
        for the corresponding vehicle.
    """,
    'author': "Grupo Leiros",
    'website': "https://grupoleiros.com",
    'category': 'Accounting',
    'version': '15.0.0.1',
    'depends': ['base', 'account', 'fleet', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_views_inherit.xml',
        'views/set_vehicles_wizard_views.xml',
        'views/fleet_vehicle_cost_views_inherit.xml',
    ],
    'installable': True,
}
