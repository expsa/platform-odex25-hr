{
    "name": 'product_negative',
    'summary': 'Only supervisor can approve POS Order with out-of-stock product',
    "category": "Point Of Sale",

    "author": "Abderrahman belhadj",

    'version': '1.0',
    'category': 'Point of Sale',

    "depends": [
        "block_by_pin",
        "product_available",
        "sale_order_product_qty",
        "sale_stock",
        "stock",
    ],

    "data": [
        'data/data.xml',
        'views/pos.xml',
        'views/product_product_views.xml',
    ],
}
