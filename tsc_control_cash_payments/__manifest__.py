# -*- coding: utf-8 -*-
{
    'name': "Control of cash payments",

    'summary': "Allows the registration of cash payments only for certain users. Automatically generate statements for cash payments to suppliers. Creates a new accounting board Kanban view, showing only cash type journals. It is accessed only by a user group",

    'description': "Allows the registration of cash payments only for certain users. Automatically generate statements for cash payments to suppliers. Creates a new accounting board Kanban view, showing only cash type journals. It is accessed only by a user group",

    'author': "Techne Studio IT & Consulting",
    'website': "https://technestudioit.com/",

    'license': "Other proprietary",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '15.0.2.0',

    # any module necessary for this one to work correctly
    'depends': ['account_accountant'],

    # always loaded
    'data': [
        'security/tsc_account_security.xml',
        'views/views.xml',
        'views/tsc_view_cash_dashboar.xml'
    ],
}
