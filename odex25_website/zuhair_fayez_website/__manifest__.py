# -*- coding: utf-8 -*-
{
    'name': "zuhair_fayez_website",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'web', 'project', 'project_custom'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/website_project_service.xml',
        'views/website_media_menu.xml',
        'views/project_project.xml',
        'views/templates.xml',
        'template/services.xml',
        'template/resources.xml',
        'template/contact.xml',
        'template/news.xml',
        'template/activites.xml',
        'template/awards.xml',
        'template/news_details.xml',
        'template/careers.xml',
        'template/job_details.xml',
        'template/service_sub_projects.xml',
        'template/project_details.xml',
        'template/service.xml',
        'template/about.xml',
        'template/index.xml',
        'template/header.xml',
        'template/footer.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
