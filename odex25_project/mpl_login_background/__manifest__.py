# -*- coding: utf-8 -*-
###############################################################################
#
#    Meghsundar Private Limited(<https://www.meghsundar.com>).
#
###############################################################################
{
    'name': 'Login Background',
    'summary': 'Configure Odoo Web Login Screen',
    'description': 'Configure Odoo Web Login Screen',
    'version': '14.0.1',
    'license': 'AGPL-3',
    'author': 'Meghsundar Private Limited',
    'website': 'https://meghsundar.com',
    'category': 'Web',
    'depends': ['base', 'base_setup', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views_inherit.xml',
        'views/image_login.xml',
        'templates/left_login_template.xml',
        'templates/right_login_template.xml',
        'templates/middle_login_template.xml',
        'templates/assets.xml',
    ],
    'images': ['static/description/banner.gif'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
