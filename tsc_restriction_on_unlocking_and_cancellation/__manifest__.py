# -*- coding: utf-8 -*-
{
    'name': "Restrictions on unlocking or cancelling sale orders, purchase orders and invoices",

    'summary': """
       Allows authorized users to unlock confirmed sales and purchase orders, return published customer and supplier invoices to draft, cancel sales orders, create, confirm and cancel customer invoices.
    """,

    'description': """
        Allows authorized users to unlock confirmed sales and purchase orders, return published customer and supplier invoices to draft, cancel sales orders, create and confirm customer invoice and cancel customer invoices that do not have confirmed shipments. All permissions are through user groups.
    """,

    'author': "Techne Studio IT & Consulting",
    'website': "https://technestudioit.com/",

    'version': '2.1',

    'license': 'Other proprietary',

    # any module necessary for this one to work correctly
    'depends': [
        'base', 
        'sale', 
        'purchase',
        'account'
    ],

    # always loaded
    'data': [
        "security/tsc_access.xml",
        'views/tsc_sale_views.xml',
        'views/tsc_purchase_views.xml',
        'views/tsc_accounting_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}