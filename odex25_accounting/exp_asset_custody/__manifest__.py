# -*- coding: utf-8 -*-
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Asset Custody Management',
    'summary': 'Custody Operations for Asset',
    'description': '''
Manage Assets transfer between locations, departments and employees
    ''',
    'version': '1.0.0',
    'category': 'Odex25 Accounting/Accounting',
    'author': 'Expert Co. Ltd.',
    'website': 'http://www.exp-sa.com',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'exp_asset_base','hr_expense_petty_cash'
    ],
    'data': [
        'data/asset_data.xml',
        'security/ir.model.access.csv',
        'views/account_asset_view.xml',
        'views/account_asset_adjustment_view.xml',
        'views/account_asset_custody_operation_view.xml',
        'views/account_asset_custody_multi_operation.xml',
        'reports/asset_adjustment_report.xml',
        'views/menus.xml'
    ],
}
