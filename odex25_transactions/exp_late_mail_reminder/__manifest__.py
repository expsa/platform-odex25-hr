# -*- coding: utf-8 -*-
##############################################################################
#
#    Odex - Communications Management System.
#    Copyright (C) 2019 Expert Co. Ltd. (<http://exp-sa.com>).
#
##############################################################################
{
    'name': 'Late Mail Reminder',
    'version': '1.0',
    'sequence': 10,
    'author': "Expert Co. Ltd. - Sudan team",
    'category': 'mail',
    'summary': 'mail reminder',
    'description': """
Late Mail Reminder
========================================
extend for stander landed costs to change work flow and to add new field""",
    'website': 'http://www.exp-sa.com',
    'depends': ['fetchmail'],
    'data': [
        'data/late_email_data.xml',
        'data/mail_data.xml',
        'views/late_mail_reminder_views.xml',
        'views/assets.xml',

    ],
    'qweb' : [
        # 'static/src/xml/notification_dialog.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
