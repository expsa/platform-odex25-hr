# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': "Telr Payment",
    'version': '14.0.0.1',
    'summary': 'Telr Payment Gateway - One of the widely used payment gateway used in the UAE integrated with odoo ecommerce | Telr Payment Gateway | Telr Payement Acquirer | Telr Payement Provider | AED Online Payment | AED Debit Card Payment | AED E-commerce payment | AED Online sale payment | AED Online card payment',
    'description': """
Telr Payment Gateway
================================
One of the widely used payment gateway used in the UAE integrated with odoo ecommerce'
    """,
    'license': 'OPL-1',
    'author': "Kanak Infosystems LLP.",
    'website': "https://kanakinfosystems.com",
    'images': ['static/description/main_image.jpg'],
    'category': 'Accounting/Payment Providers',
    'depends': ['website_sale'],
    'data': [
        'views/payment_templates.xml',
        'views/payment_views.xml',
        'data/data.xml',
    ],
    'application': True,
    'installable': True,
    'price': 65,
    'currency': 'EUR'
}
