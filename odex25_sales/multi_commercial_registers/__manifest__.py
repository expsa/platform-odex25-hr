# -*- coding: utf-8 -*-
{
    'name': 'Multi Commercial Registers',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Multi Commercial Registers',
    'description': """Multi Commercial Registers""",
    'depends': ['point_of_sale', 'branch', 'bi_branch_pos', 'report_e_invoice_pos', 'account'],
    'data': [
        'views/branch_view.xml',
        'views/pos_session.xml',
        'views/pos_config.xml',
        'views/account_invoice.xml',
        'reports/e_invoice.xml',
    ],
    'qweb': ['static/src/xml/pos_receipt.xml'],

    'installable': True,
    'auto_install': False,
}
