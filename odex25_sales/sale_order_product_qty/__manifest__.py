# -*- coding: utf-8 -*-
{
    'name': "sale_order_product_qty",

    'description': """
        show Qty available in the sale order.
    """,

    'author': "Abderrahman Belhadj",
    # 'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'stock', 'sale_stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_view.xml',
    ],
}