{
    "name": """product_available""",
    "summary": """Adds Quantity label to each product in POS""",
    "category": "Point Of Sale",

    "author": "Abdurrahman Saber",

    'version': '14.0',
    'category': 'Point of Sale',

    "depends": [
        'point_of_sale',
        'stock',
    ],

    'data': [
        'data/data.xml',
        'views/views.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ]

}
