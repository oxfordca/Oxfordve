# -*- coding: utf-8 -*-
{
    'name': "Asignación y Consumo de Equipos y Materiales",

    'summary': """
        Permite registra la asignación y consumo de equipos y materiales empleados de manera interna.
    """,

    'description': """
        Incluye movimientos de inventario y campos adicionales, que permiten el
registro de consumo de equipos y materiales, así como la asignación de los mismos a
empleados, departamentos o vehículos. Incluye un indicador en la vista Kanban de productos
que indica la cantidad de productos libres para ser asignados. Para el correcto comportamiento de este módulo, debe estar instalado: tsc_adjustments_for_internal_purchases.
    """,

    'author': "Techne Studio IT & Consulting",
    'website': "https://technestudioit.com/",

    'category': 'Inventory',
    'version': '2.2',

    'license': 'Other proprietary',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','branch','hr','fleet'],

    # always loaded
    'data': [
        'security/acceso_transferencias_internas.xml',
        'data/stock_locations.xml',
        'data/mov_asignacion.xml',
        'data/mov_consumo.xml',
        'data/mov_asignacion_y_consumo.xml',
        'views/stock_pick_type_views.xml',
        'views/stock_move_line_views.xml',
        'views/tsc_stock_location_views.xml',
        'views/tsc_product_template_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
