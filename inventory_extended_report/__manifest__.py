# -*- coding: utf-8 -*-
{
    'name': "Inventory Extended Report",
    'description': """
        Extension del reporte de 'Informe de inventario', 
        agrega los campos de box_cero, box_uno y box_dos en los modelos
        de product.template y product.product
    """,
    'author': "Adrian Alves",
    'website': "",
    'category': 'Customizations',
    'version': '15.0.0.2',
    'depends': ['base', 'product', 'account', 'stock', 'stock_replenishment_report'],
    'data': [
        'security/security.xml',
        'views/product_template_views_inherit.xml',
        'views/product_views_inherit.xml',
    ],
    'demo': [],
}
