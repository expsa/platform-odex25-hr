# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from num2words import num2words
from odoo import api, exceptions, fields, models


class HrEmployeeSalaryScale(models.Model):
    _inherit = 'hr.employee'

    salary_scale = fields.Many2one(related='contract_id.salary_scale', string='Salary scale', store=True)
    salary_level = fields.Many2one(related='contract_id.salary_level', string='Salary Level', store=True)
    salary_group = fields.Many2one(related='contract_id.salary_group', string='Salary Group', store=True)
    salary_degree = fields.Many2one(related='contract_id.salary_degree', string='Salary Degree', store=True)
    base_salary = fields.Float(compute='compute_base_salary')
    salary_in_words = fields.Char(compute='get_salary_amount')
    payslip_lines = fields.One2many(comodel_name='hr.payslip.line', compute='compute_base_salary')

    @api.depends('base_salary')
    def get_salary_amount(self):
        for item in self:
            item.salary_in_words = num2words(item.base_salary, lang=self.env.user.lang)

    def compute_base_salary(self):
        for item in self:
            last_day_of_prev_month = datetime.now().date().replace(day=1) - timedelta(days=1)
            start_day_of_prev_month = datetime.now().date().replace(day=1) - timedelta(days=last_day_of_prev_month.day)

            payroll = item.env['hr.payslip'].search(
                [('employee_id', '=', item.name), ('date_from', '<=', datetime.now().date()),
                 ('date_to', '>=', datetime.now().date()), ('contract_id', '=', item.contract_id.id)], limit=1)
            if not payroll:
                payroll = item.env['hr.payslip'].search(
                    [('employee_id', '=', item.name), ('date_from', '<=', start_day_of_prev_month),
                     ('date_to', '>=', last_day_of_prev_month), ('contract_id', '=', item.contract_id.id)], limit=1)

            item.base_salary = payroll.total_allowances
            item.payslip_lines = payroll.allowance_ids.filtered(
                lambda r: r.salary_rule_id.rules_type in ('salary', 'house', 'transport', 'other')).sorted(
                lambda b: b.name)
