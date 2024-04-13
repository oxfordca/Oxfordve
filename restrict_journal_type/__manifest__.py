# -*- coding: utf-8 -*-
{
    'name': "Restricciones por tipo de diario.",

    'summary': """
        Incluye una clasificación para los diarios, identificándolos como “Custodio” e “Inversión”, a fin de que sólo ciertos usuarios puedan visualizar dichos diarios""",

    'description': """
       Incluye una clasificación para los diarios, identificándolos como “Custodio” e “Inversión”, a fin de que sólo ciertos usuarios puedan visualizar dichos diarios. Agrega los grupos de usuario: Visualizar diarios de tipo Custodio y Visualizar diarios de tipo Inversión.

       Se eliminaron los siguientes permisos de acceso:
        1. access_investment_type_journal
        2. access_custodian_type_journal

       Se eliminaron las siguientes reglas de registro:
        1. Visualizar diarios de tipo inversión
        2. Visualizar diarios de tipo custodio
        3. Visualizar diarios sin tipo asigando
    """,

    'author': "Techne Studio IT & Consulting",
    
    'website': "https://technestudioit.com/",
  
    'category': 'Accounting/Accounting',

    'version': '15.0.2.0',

    'license': "Other proprietary",

    'depends': ['base', 'account'],

    "installable": True,
    
    "data": [            
            'security/restrict_journal_type.xml',
            # 'security/ir.model.access.csv',
            'views/journal_type.xml',       
        ],
}
