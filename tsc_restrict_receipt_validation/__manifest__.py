# -*- coding: utf-8 -*-
{
    'name': "Restrict receipt validation",

    'summary': """
       Allows the validation of merchandise-reception operations only by authorized users.
    """,

    'description': """
        Allows the validation of merchandise-reception operations only by authorized users. Create a new user group for said
validation.
    """,

    'author': "Techne Studio IT & Consulting",
    
    'website': "https://technestudioit.com/",

    'version': '1.0',
    
    'category': 'Inventory',
    
    'license': 'Other proprietary',

    # any module necessary for this one to work correctly
    'depends': [
        'base', 
        'stock',
    ],

    # always loaded
    'data': [
        'security/tsc_access.xml',
    ],
    
    # only loaded in demonstration mode
    'demo': [
    ],
}