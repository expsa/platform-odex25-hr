# Copyright 2021 Khabir
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Report E Invoice POS',
    'description': """
        E-Invoice Report POS""",
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Expert Co. Ltd.',
    'website': 'http://www.exp-sa.com',
    'depends': ['report_e_invoice', 'point_of_sale'],
    'data': [
        'views/templates.xml',
    ],
    'qweb': [
        'static/src/xml/pos_receipt.xml',
    ],
}
