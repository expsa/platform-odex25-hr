# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class HrOvertimeReportOfEmployee(models.TransientModel):
    _name = "overtime.report.of.employee"
    _description = "Overtime report of employee"

    date_from = fields.Datetime()
    date_to = fields.Datetime()
    department_id = fields.Many2one('hr.department')
    job_id = fields.Many2one('hr.job')

    def get_report(self):
        """Call when button 'Get Report' clicked.
        """
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_from,
                'date_end': self.date_to,
                'department_id': self.department_id.id,
                'job_id': self.job_id.id,
            },
        }

        return self.env.ref('hr_base_reports.action_report_overtime').report_action(self, data=data)

    def get_reportxlsxs(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_from,
                'date_end': self.date_to,
                'department_id': self.department_id.id,
                'job_id': self.job_id.id,
            },
        }
        return self.env.ref('hr_base_reports.action_report_overtime_xlsx').report_action(self, data=data)


class ReportHrPenaltyDeductionOfEmployee(models.AbstractModel):
    """Abstract Model for report template.
    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = 'report.hr_base_reports.report_overtime_requests_template'
    _description = "Employee Overtime Requests Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = datetime.strptime(data['form']['date_start'], DATETIME_FORMAT)
        date_end = datetime.strptime(data['form']['date_end'], DATETIME_FORMAT) + timedelta(days=1)
        department = data['form']['department_id']
        job = data['form']['job_id']

        docs = []

        overtime = self.env['employee.overtime.request'].search([
            ('create_date', '>=', date_start.strftime(DATETIME_FORMAT)),
            ('create_date', '<', date_end.strftime(DATETIME_FORMAT))
        ])
        for item in overtime:
            if item.employee_id.department_id.id == department or item.employee_id.job_id.id == job:
                docs.append({
                    'employee': item.line_ids_over_time.employee_id.name,
                    'department': item.department_id.name,
                    'job': item.line_ids_over_time.employee_id.job_id.name,
                    'hours_number': item.line_ids_over_time.over_time_workdays_hours + item.line_ids_over_time.over_time_vacation_hours,
                })
            else:
                docs.append({
                    'employee': item.line_ids_over_time.employee_id.name,
                    'department': item.department_id.name,
                    'job': item.line_ids_over_time.employee_id.job_id.name,
                    'hours_number': item.line_ids_over_time.over_time_workdays_hours + item.line_ids_over_time.over_time_vacation_hours,
                })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start.strftime(DATE_FORMAT),
            'date_end': (date_end - timedelta(days=1)).strftime(DATE_FORMAT),
            'docs': docs,
        }


class HrOvertimeJobParseXlsx(models.AbstractModel):
    _name = "report.hr_base_reports.action_report_overtime_xlsx"
    _description = "XLSX Employee Overtime Requests Report"
    _inherit = 'report.report_xlsx.abstract'

    @api.model
    def generate_xlsx_report(self, workbook, data, objs):
        date_start = datetime.strptime(data['form']['date_start'], DATETIME_FORMAT)
        date_end = datetime.strptime(data['form']['date_end'], DATETIME_FORMAT) + timedelta(days=1)
        department = data['form']['department_id']
        job = data['form']['job_id']

        docs = []

        overtime = self.env['employee.overtime.request'].search([
            ('create_date', '>=', date_start.strftime(DATETIME_FORMAT)),
            ('create_date', '<', date_end.strftime(DATETIME_FORMAT))
        ])
        for item in overtime:

            if item.department_id.id == department or item.employee_id.job_id.id == job:
                docs.append({
                    'employee': item.line_ids_over_time.employee_id.name,
                    'department': item.department_id.name,
                    'job': item.line_ids_over_time.employee_id.job_id.name,
                    'hours_number': item.line_ids_over_time.over_time_workdays_hours + item.line_ids_over_time.over_time_vacation_hours,
                })
            else:
                docs.append({
                    'employee': item.line_ids_over_time.employee_id.name,
                    'department': item.department_id.name,
                    'job': item.line_ids_over_time.employee_id.job_id.name,
                    'hours_number': item.line_ids_over_time.over_time_workdays_hours + item.line_ids_over_time.over_time_vacation_hours,
                })

        sheet = workbook.add_worksheet('Termination of employees')
        format1 = workbook.add_format(
            {'font_size': 10, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'center',
             'bold': True})
        format2 = workbook.add_format(
            {'font_size': 10, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'center',
             'bold': True})
        format2.set_align('center')
        format2.set_align('vcenter')
        format1.set_font_color('black')
        format1.set_fg_color('#e6e6e6')
        format2.set_font_color('#464dbb')
        format2.set_fg_color('#e6e6ff')

        sheet.write('A3:A3', 'Employee', format2)
        sheet.write('B3:B3', 'Jobs', format2)
        sheet.write('C3:C3', 'Department', format2)
        sheet.write('D3:D3', 'Number of Hours', format2)
        # sheet.write('E3:E3', 'Holiday type', format2)
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        # sheet.set_column('E:E', 20)

        row = 3
        col = 0
        for line in docs:
            row += 1
            sheet.write(row, col, line['employee'], format1)
            sheet.write(row, col + 1, line['job'], format1)
            sheet.write(row, col + 2, line['department'], format1)
            sheet.write(row, col + 3, line['hours_number'], format1)

