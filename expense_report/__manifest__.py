# -*- coding: utf-8 -*-
{
    'name': "Expense Report",
    'summary': """
        Adds a view where the accounting entries of the 'expense' type accounts are displayed.
    """,
    'description': """
        Adds a new title in the 'reports' section in accounting called 'Expense Report' where the accounting entries 
        of the 'expense' type accounts will be displayed.
    """,
    'author': "Grupo Leiros",
    'website': "https://grupoleiros.com",
    'category': 'Accounting',
    'version': '15.0.0.1',
    'depends': ['base', 'account', 'web', 'branch', 'show_account_menu'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_line_views.xml',
        'views/account_move_line_action.xml',
        'wizard/filter_date_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'expense_report/static/src/legacy/js/views/**/*',
        ],
    },
    'installable': True,
}
