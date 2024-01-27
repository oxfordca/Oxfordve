# -*- coding: utf-8 -*-
{
    'name': "Restriction to confirm customer credit note",

    'summary': "Restricts the ability to create and confirm customer credit notes, allowing only authorized users.",

    'description': "Restricts the ability to create and confirm customer credit notes, allowing only authorized users.",

    'author': "Techne Studio IT & Consulting",
    'website': "https://technestudioit.com/",

    'license': "Other proprietary",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '2.0',

    # any module necessary for this one to work correctly
    'depends': ['account_accountant'],

    # always loaded
    'data': [
        'views/views.xml',
        'security/tsc_access.xml',
    ],
}
