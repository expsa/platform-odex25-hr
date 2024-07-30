# -*- coding: utf-8 -*-
{
    'name': 'HR Advance Payroll',
    'version': '1.0',
    'category': 'HR-Odex',
    'sequence': 4,
    'website': 'http://exp-sa.com',
    'license': 'GPL-3',
    'author': 'Expert Co. Ltd.',
    'summary': 'Advance Payroll In HR',
    'description': """
       Helps you to manage All Payroll Requests of your company's staff.
        """,
    'depends': [
        'exp_hr_payroll',
        'hr_holidays_community',
        'account',
        'report_xlsx',
        'hr_contract_custom'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/data.xml',

        'views/salary_structure.xml',
        # 'views/salary_advance.xml',
        'views/payslip_view.xml',
        'views/employee_promotions_view.xml',
        'views/hr_salary_rules.xml',
        'views/hr_salary_scale.xml',
        'views/salary_scale_level_group.xml',
        'views/hr_salary_scale_level.xml',
        'views/hr_salary_scale_level_degree.xml',
        'views/hr_recontract.xml',
        'views/hr_employee.xml',
        'views/hr_contract.xml',
        'views/employee_reward_view.xml',
        'views/payroll_report.xml',
        'views/contract_advantage.xml',

        # menus
        'views/payroll_menus.xml',
        'views/hr_salary_menus.xml',
        'wizard/payslip_monthly_report_view.xml',
        'wizard/payroll_bank_report_view.xml',

        # reports templates
        'templates/hr_payslip_run_template.xml',
        'templates/payslip_monthly_report.xml',
        'templates/report_payslip_details.xml',
        'templates/report_payslip.xml',
        'templates/bank_pdf_report.xml',
        'templates/employee_cost_template.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
