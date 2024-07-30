# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    "name": "Drag & Drop Multi Attachments",
    "version": "14.0",
    'author': "Expert Co. Ltd.",
    'website': "http://www.exp-sa.com",
    "category": "Social Network",
    "summary": "Drag & Drop multiple attachments in the form view at once",
    "description": """
    This module enables the feature to Drag & Drop multiple attachments in the form view of any objects.

    The attachments which are selected can simply drag &amp; drop to the form view and will be available at the "Attachments" dropdown box on the top of the form view.

    To attach the files in the Odoo object, You have to open the form view, explore the file(s), select the file(s) and drag & drop them into the “Drop your files here” area of the form view.

    Dropped files will be available in the “Attachments” dropdown box on the top of the form view.
    """,
    "depends": ["documents"],
    'data': ["views/drag_drop_attach_view.xml"],
    'images': [
        'static/description/main_screen.jpg'
    ],
    "price": 50,
    "currency": "EUR",
    "installable": True,
    "auto_install": False,
    'license': '',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
