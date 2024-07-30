# -*- coding: utf-8 -*-
{
    'license': 'LGPL-3',
    'name': "Web Window Title",
    'summary': "The custom web window title",
    'author': "renjie <i@renjie.me>",
    'website': "https://renjie.me",
    'support': 'i@renjie.me',
    'category': 'Extra Tools',
    'version': '1.1',
    'depends': ['base', 'base_setup', 'point_of_sale', 'web', 'odex25_web'],
    'demo': [
        'data/demo.xml',
    ],
    'data': [
        'views/webclient_templates.xml',
        'views/res_config.xml',
        'views/web_login.xml',
    ],
    "qweb": [
        "static/src/xml/custom_template.xml",
        "static/src/xml/error.xml",
        "static/src/xml/odoo_error_header.xml",
    ],
    'images': [
        'static/description/main_screenshot.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
