# -*- coding: utf-8 -*-
{
    'name': "odex25 Purchase Saip",
    'version': "1.0",
    'category': 'Odex25 Inventory/Purchase',
    'author': 'Expert Co. Ltd.',
    'website': 'http://www.exp-sa.com',
    'summary': "Advanced Features for Purchase Management",
    'description': """
            Contains advanced features for purchase management
    """,
    # any module necessary for this one to work correctly
    'depends': ['purchase_requisition_custom','governmental_purchase','account_budget_custom','online_tendering'],

    # always loaded
    'data': [
        'security/purchase_request_security.xml',
        'data/purchase_request_seq.xml',
        'views/assets.xml',
        'views/budget_confirmation_view.xml',
        'views/purchase_request.xml',
        'views/res_setting.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
