# -*- coding: utf-8 -*-
{
    'name': "inventory_product_qty",

    'description': """
        show Qty available in the inventory adjustment.
    """,

    'author': "Expert Co. Ltd.",
    'category': 'Stock',
    'version': '14.0.0',
    'depends': ['base', 'stock'],
    'data': [
        'views/stock_move_line.xml',
    ],
}
