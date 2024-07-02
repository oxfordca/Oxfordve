# -*- coding: utf-8 -*-
{
    'name': "restrict_inventory_adjustments",
    'description': "Añade un grupo de usuarios para restringir las acciones de usuarios en los ajustes de inventario",
    'author': "Adrian Alves",
    'website': "",
    'category': 'Inventory',
    'version': '15.0.1',
    'depends': ['base', 'stock'],
    'data': [
        'security/security_group.xml',
        'views/stock_quant_views.xml',
    ],
    'installable': True,
}
