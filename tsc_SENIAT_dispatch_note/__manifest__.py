# -*- coding: utf-8 -*-
{
    'name': "SENIAT format dispatch note",

    'summary': """
        Includes a new delivery note report for internal transfers, according to the format required by SENIAT
    """,

    'description': """
        Includes a new delivery note report for internal transfers, according to the format required by SENIAT. Includes control number, reason for transfer and currency fields to complete the information required in the form
    """,

    'author': "Techne Studio IT & Consulting",
    'website': "https://technestudioit.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory/Inventory',
    'version': '15.0.2.2',
    'license': 'Other proprietary',
    # any module necessary for this one to work correctly
    'depends': ['base', 'branch', 'sequences_for_OS_and_guides'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/tsc_security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/tsc_stock_picking_views.xml',
        'report/tsc_stock_report_views.xml',
        'report/tsc_report_dispatch_note.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
