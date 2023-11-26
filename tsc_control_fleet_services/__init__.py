# -*- coding: utf-8 -*-

from . import controllers
from . import models
from odoo import api, SUPERUSER_ID

def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    env['ir.model.access'].search([('name', '=', 'fleet_vehicle_cost_report_access_right')]).write({
        'perm_read': True,
        'perm_write': True,
        'perm_create': True,
        'perm_unlink': True,
    })