# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

import datetime
from datetime import datetime

from pprint import pprint
import xlsxwriter


class HrTerminationWizard(models.TransientModel):
    _name = "hr.termination.wizard"
    _description = "termination Wizard"

    date_from = fields.Datetime()
    date_to = fields.Datetime()
    cause_type = fields.Many2one('hr.termination.type')

    def get_report(self):
        """Call when button 'Get Report' clicked.
        """
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_from,
                'date_end': self.date_to,
                'cause_type': self.cause_type.id,
            },
        }
        return self.env.ref('hr_base_reports.action_report_termination').report_action(self, data=data)

    def get_reportxlsxs(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_from,
                'date_end': self.date_to,
                'cause_type': self.cause_type.id,
            },
        }
        return self.env.ref('hr_base_reports.action_report_termination_xlsx').report_action(self, data=data)


class ReportHrTerminationWizard(models.AbstractModel):
    """Abstract Model for report template.
    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = 'report.hr_base_reports.report_termination_template'
    _description = "Termination Template Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = datetime.strptime(data['form']['date_start'], DATETIME_FORMAT)
        date_end = datetime.strptime(data['form']['date_end'], DATETIME_FORMAT) + timedelta(days=1)
        cause_type = data['form']['cause_type']
        docs = []
        termination = self.env['hr.termination'].search([
            ('create_date', '>=', date_start.strftime(DATETIME_FORMAT)),
            ('create_date', '<', date_end.strftime(DATETIME_FORMAT)),
            ('cause_type', '=', cause_type),
        ])
        for item in termination:
            docs.append({
                'employee': item.employee_id.name,
                'job': item.job_id.name,
                'department': item.department_id.name,
                'cause_type': item.cause_type.name,
                'reason': item.reason,
            })
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start.strftime(DATE_FORMAT),
            'date_end': (date_end - timedelta(days=1)).strftime(DATE_FORMAT),
            'docs': docs,
        }


class HrTerminationJobParseXlsx(models.AbstractModel):
    _name = "report.hr_base_reports.action_report_termination_xlsx"
    _description = "XLSX Termination Report"
    _inherit = 'report.report_xlsx.abstract'

    @api.model
    def generate_xlsx_report(self, workbook, data, objs):
        date_start = datetime.strptime(data['form']['date_start'], DATETIME_FORMAT)
        date_end = datetime.strptime(data['form']['date_end'], DATETIME_FORMAT) + timedelta(days=1)
        cause_type = data['form']['cause_type']

        docs = []

        termination = self.env['hr.termination'].search([
            ('create_date', '>=', date_start.strftime(DATETIME_FORMAT)),
            ('create_date', '<', date_end.strftime(DATETIME_FORMAT)),
            ('cause_type', '=', cause_type)
        ])

        for item in termination:
            docs.append({
                'employee': item.employee_id.name,
                'job': item.job_id.name,
                'department': item.department_id.name,
                'cause_type': item.cause_type.name,
                'reason': item.reason,

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
        format1.set_font_color('gray')
        format1.set_fg_color('#e6e6e6')
        format2.set_font_color('#464dbb')
        format2.set_fg_color('#e6e6ff')
        sheet.write('A3:A3', 'Employee', format2)
        sheet.write('B3:B3', 'Jobs', format2)
        sheet.write('C3:C3', 'Department', format2)
        sheet.write('D3:D3', 'Cause type', format2)
        sheet.write('E3:E3', 'Reason', format2)
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)

        row = 3
        col = 0
        for line in docs:
            row += 1
            sheet.write(row, col, line['employee'], format1)
            sheet.write(row, col + 1, line['job'], format1)
            sheet.write(row, col + 2, line['department'], format1)
            sheet.write(row, col + 3, line['cause_type'], format1)
            sheet.write(row, col + 4, line['reason'], format1)
