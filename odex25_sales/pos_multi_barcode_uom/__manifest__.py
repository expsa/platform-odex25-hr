# -*- coding: utf-8 -*-

{
    'name': 'pos_multi_barcode_uom',
    'version': '14.0.1',
    'category': 'Point of Sale',

    'author': 'Abderrahman Belhadj',
    'summary': 'Barcode and Price for different unit of measure.',

    'depends': ['point_of_sale', 'branch'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml'
    ],
    'qweb': [
        'static/src/xml/ProductScreen/ControlButtons/ChangeuomButton.xml',
    ],

}
