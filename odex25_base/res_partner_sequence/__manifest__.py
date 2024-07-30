# -*- coding: utf-8 -*-
{
    'name': "res_partner_sequence",

    'summary': """
        Add Partner Sequence
    """,
    'description': """
        Add Partner Sequence
    """,
    'author': "Abderrahman Belhadj",

    'category': 'base',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/res_partner.xml',
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
    ],
}