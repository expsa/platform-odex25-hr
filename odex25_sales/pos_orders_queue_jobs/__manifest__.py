# -*- coding: utf-8 -*-
{
    'name': "PoS Orders Queue Jobs",

    'summary': """
        Delay the creation of Pickings and Invoices of PoS orders and the closing of PoS sessions""",

    'author': "Abdelrahman Khaled",

    'category': 'Point Of Sale',
    'version': '0.1',

    'data': [
        'data/queue_job_channels_data.xml'
    ],

    'depends': ['queue_job', 'point_of_sale'],
}