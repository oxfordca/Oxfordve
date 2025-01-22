# -*- coding: utf-8 -*-
{
    'name': "Invoice Amounts Widget",
    'summary': """
        Add amounts to the invoice form view
    """,
    'description': """
        Adds amounts to the invoice form view that are manually set by the user.
    """,
    'author': "Grupo Leiros",
    'website': "https://grupoleiros.com",
    'category': 'Accounting',
    'version': '15.0.0.1',
    'depends': ['base', 'account'],
    'data': [
        'views/account_move_views_inherit.xml',
    ],
    'installable': True,
}
