# -*- coding: utf-8 -*-
{
    'name': "hide_cost_price",

    'description': """
        Hide cost Price from users
    """,

    'author': "Abderrahman Belhadj // Sinen Ben Amor",
    # 'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_margin', 'stock_account', 'product'],

    # always loaded
    'data': [
        'views/security.xml',
        'views/sale_order.xml',
        'views/product_template.xml',
    ],
}
