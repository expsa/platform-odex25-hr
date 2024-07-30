{
    "name": """POS Orders Return""",
    "summary": """The module allows to make order returns from POS interface by quick & easy way""",
    "category": "Point of Sale",
    "images": ["images/pos_orders_return_main.jpg"],
    "version": "14.0.1.0",
    "application": False,
    "author": "Odex.sa",
    "support": "odex.sa",
    "website": "odex.sa",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["pos_orders_history", "point_of_sale", "product_available"],
    "data": [
        "views/pos_orders_history_return_view.xml",
        "views/pos_orders_history_return_template.xml",
    ],
    "qweb": [
        "static/src/xml/pos.xml",
    ],
}
