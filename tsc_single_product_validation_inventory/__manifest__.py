# -*- coding: utf-8 -*-
{
    'name': "Validation of single product in inventory",

    'summary': """
       Validates that a product is not repeated in internal inventory transfers.
    """,

    'description': """
        Validates that a product is not repeated in internal inventory transfers.
    """,

    'author': "Techne Studio IT & Consulting",
    'website': "https://technestudioit.com/",

    'category': 'Inventory',

    'version': '1.1',

    'license': 'Other proprietary',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        "views/tsc_stock_picking_views.xml",
    ],

    # only loaded in demonstration mode
    'demo': [
    ],


    
}
