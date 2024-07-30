# -*- coding: utf-8 -*-
{
    'name': "HR Custody Integration With Asset Custody",

    'summary': """
      - Assign Asset as a custody to an employee
      - Release Asset as a custody from an employee
      """,
    'version': '14.0',
    'sequence': 4,
    'category': 'ODEX ACCOUNTING',
    'website': 'http://exp-sa.com',
    'license': 'AGPL-3',
    'author': 'Expert Co. Ltd.',
    'depends': ['exp_employee_custody','exp_asset_custody','purchase_requisition_custom'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/employee_custody_action.xml',
    ],

}