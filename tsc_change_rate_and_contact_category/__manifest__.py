# -*- coding: utf-8 -*-
{
    'name': "Change rate and contact category",

    'summary': "Allows changing the rate and category of a contact only for authorized users.",

    'description': "Allows changing the rate and category of a contact only for authorized users.",

    'author': "Techne Studio IT & Consulting",
    'website': "https://technestudioit.com/",

    'license': "Other proprietary",

    'version': '1.0',

    'depends': [
        'base', 
        'product',
    ],

    'data': [
        'security/tsc_access.xml',
        'views/tsc_res_partner_views.xml',
    ],
}
