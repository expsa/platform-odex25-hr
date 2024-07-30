# -*- coding: utf-8 -*-
{
    'name': "Sales Terms&Conditions",
    'author': "Expert Co. Ltd.",
    'website': 'http://exp-sa.com',
    'category': 'Sales',
    'version': '11.1.0.1',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/terms_conditions_view.xml',
        'views/sale_order_view.xml',
        'wizard/sale_setting_wiz_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,

}
