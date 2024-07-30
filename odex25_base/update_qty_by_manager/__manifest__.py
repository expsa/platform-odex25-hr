# -*- coding: utf-8 -*-
{
    'name': "update_qty_by_manager",

    'description': """
        Update stock quantity on by inventory manager
    """,

    'author': "Abderrahman Belhadj",
    # 'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'views/security.xml',
        'views/product_product.xml',
    ],
}