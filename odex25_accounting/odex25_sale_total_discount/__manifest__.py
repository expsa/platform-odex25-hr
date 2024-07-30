# -*- coding: utf-8 -*-
{
    'name': "Sale Total Discount",
    'summary': """Add universal discount in sale and invoice screens""",
    'category': 'Odex25 Accounting/Accounting',
    'author': "Expert Co. Ltd.",
    'website': "http://www.exp-sa.com",
    'version': '14.0.1',
    'depends': ['base', 'sale_management', 'account', 'point_of_sale'],
    'data': [
        'data/decimal_precision.xml',
        'views/account_move_view.xml',
        'views/sale_view.xml',
        'views/pos_config_views.xml',
        'views/assets.xml',
    ],
    'qweb':[
        'static/src/xml/Screens/ProductScreens/TotalDiscount.xml'
    ] 
}
