# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

{
    'name': 'Applepay Payment Acquirer',
    'category': 'Accounting',
    'version': '14.0.0.2',
    'summary': 'Payment Acquirer: Applepay',
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'sequence': 1,
    'website': 'http://www.technaureus.com/',
    'description': """Applepay Payment Acquirer""",
    'price': 79.99,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',
        'views/payment_popup_template.xml',
        'views/payment_applepay_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'images': ['images/main_screenshot.gif'],
    'installable': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
}
