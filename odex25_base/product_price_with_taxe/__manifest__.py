# -*- coding: utf-8 -*-
{
    'name': "product_price_with_taxe",

    'summary': """
        Compute Taxes on product""",

    'description': """
        Made with Love by Abdou Bhj
    """,

    'author': "Abderrahman Belhadj",
    'category': 'Product',
    'version': '14.0',

    'depends': ['product', 'account', 'dynamic_barcode_labels'],

    'data': [
        'views/inherit_product.xml',
        'views/inherit_barcode_config.xml',
    ],
}
