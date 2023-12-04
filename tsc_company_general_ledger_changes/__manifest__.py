# -*- coding: utf-8 -*-
{
    'name': "Changes in general ledger by company",

    'summary': """
        Includes an Estimated Receipt, Products Received, and Products in Transit date column for supplier invoice records in a company's General Ledger. Make a distinction by color according to the state of receipt of the merchandise""",

    'description': """
        Includes an Estimated Receipt, Products Received, and Products in Transit date column for supplier invoice records in a company's General Ledger. Make a distinction by color according to the state of receipt of the merchandise. Includes a user group that can specify whether the products of a purchase order are in transit
    """,

    'author': "Techne Studio IT & Consulting",
    'website': "https://technestudioit.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.1.1',
    'license': "Other proprietary",

    # any module necessary for this one to work correctly
    'depends': ['base', 'tsc_mark_products_received', 'branch_accounting_report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'security/tsc_security.xml',
        'views/tsc_purchase_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
