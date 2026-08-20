# -*- coding: utf-8 -*-
{
    'name': "Restrict customer invoice edition",

    'summary': """
Prevents users from altering invoice lines, products, quantities, prices and units of measure, allowing only the editing of administrative fields.
    """,

    'description': """
Restricts users from modifying critical data in customer invoices. Once an invoice is generated from a confirmed Sale Order, the system blocks any alteration of invoice lines, including the editing of products, quantities, prices, and units of measure, even when the invoice is in 'Draft' state. Access is strictly limited to administrative control fields, such as Invoice Date, Taxes, and Control Number, ensuring that billing remains an exact reflection of the agreed sales terms.
    """,

    'author': "Techne Studio IT & Consulting",
    'website': "https://technestudioit.com/",

    'category_id': 'Uncategorized',
    'version': '15.0.1.1',

    'license': 'Other proprietary',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale',
       'account',
'branch',
    ],

    # always loaded
    'data': [
        'security/security.xml',
        'views/account_move_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'tsc_restrict_customer_invoice_edition/static/src/scss/tsc_restrict_customer_invoice_edition.scss',
            'tsc_restrict_customer_invoice_edition/static/src/js/tsc_restrict_customer_invoice_edition.js',
        ],
    },

    # only loaded in demonstration mode
    'demo': [
    ],
}


