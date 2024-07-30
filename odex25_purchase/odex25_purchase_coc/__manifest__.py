# -*- coding: utf-8 -*-
{
    'name': "Purchase CoC",

    'summary': """
        This Module is Designed and Developed to Add CoC process To purchase""",

    'description': """
        
    """,

    'author': "Expert CO Ltd",
    'website': "http://www.exp-sa.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['purchase_requisition_custom'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'sequence/seq.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
