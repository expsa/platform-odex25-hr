{
    'name': 'Point of Sale Logo',

    'summary': """Logo For Every Point of Sale Screen""",
    'description': """"This module helps you to set a logo for every point of sale. This will help you to
                 identify the point of sale easily. You can also see this logo in pos screen.""",
    'category': 'Point Of Sale',
    'author': 'Abderrahman Belhadj',

    'depends': ['base', 'point_of_sale'],
    'data': [
        'views/pos_config_image_view.xml',
        'views/pos_image_view.xml',
    ],

    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
