# -*- coding: utf-8 -*-
{
    'name': "incoming_qty_in_product_template",
    'description': """
        Muestra la cantidad entrante en la vista de productos
    """,
    'author': "Adrian Alves",
    'website': "",
    'category': 'Product',
    'version': '1.0',
    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],
    # always loaded
    'data': [
        'views/product_views_inherit.xml',
    ],
    'demo': [],
}
