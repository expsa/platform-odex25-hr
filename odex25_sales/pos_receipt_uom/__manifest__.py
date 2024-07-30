# -*- coding: utf-8 -*-
{
    'name': "pos_receipt_uom",

    'description': """
        Add UOM to the pos receipt
    """,

    'author': "Abderrahman Belhadj",

    'category': 'point of sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['pos_multi_barcode_uom', 'report_e_invoice_pos'],

    'qweb': [
        'static/src/xml/receipt.xml',
    ],
}
