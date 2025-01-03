# -*- coding: utf-8 -*-
{
    'name': "Import Summary",
    'summary': """
        Adds a new view in Accounting/Providers called Import Summary.
    """,
    'description': """
        This view brings the invoice number of suppliers that were marked with the 'import' check. 
        The rest of the view is editable by the user.
    """,
    'author': "Grupo Leiros",
    'website': "https://grupoleiros.com",
    'category': 'Accounting',
    'version': '15.0.0.2',
    'depends': ['base', 'account', 'purchase_stock', 'branch', 'tsc_company_general_ledger_changes', 'tsc_mark_products_received'],
    'data': [
        'security/ir.model.access.csv',
        'security/security_group.xml',
        'views/import_summary_views.xml',
        'views/account_move_views_inherit.xml',
        'views/import_summary_views_action.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'import_summary/static/src/css/custom_class.css',
            'import_summary/static/src/js/import_summary_custom.js',
        ],
    },
    'installable': True,
}
