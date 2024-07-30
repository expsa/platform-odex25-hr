# -*- coding: utf-8 -*-
{
    'name': "Stock Custom SOCPA",

    'summary': """
        Stock Cutomized module for Socpa""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock', 'exchange_request'],

    # always loaded
    'data': [
        'data/sequence_data.xml',
        'security/category_groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'views/views.xml',
        'views/stock_inventory_views.xml',
        'views/stock_scrap_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}