# -*- coding: utf-8 -*-
{
    'name': "Control in fleet services",

    'summary': "Restricts the ability to view, confirm and cancel vehicle services to authorized users only. Restricts the Reports menu option to authorized users only. Includes new vehicle information and vehicle maintenance fields.",

    'description': "Restricts the ability to view vehicle services to authorized users only. Create a new status of “Confirmed”. Restricts the ability to change the status of a service to Confirmed or Canceled to authorized users only. Restricts the Reports menu option to authorized users only. Includes new vehicle information and vehicle maintenance fields.",

    'author': "Techne Studio IT & Consulting",
    'website': "https://technestudioit.com/",

    'license': "Other proprietary",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Fleet',
    'version': '2.0',

    # any module necessary for this one to work correctly
    'depends': ['fleet', 'contacts'],

    # always loaded
    'data': [
        'views/fleet_views.xml',
        'views/contact_views.xml',
        'security/ir.model.access.csv',
    ],

    'uninstall_hook': 'uninstall_hook',
}
