# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
from dateutil import relativedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError, AccessError, UserError


class ExchangeRequestReport(models.AbstractModel):
    _name = "report.stock_custom_reports.exchange_request_report"

    @api.model
    def _get_report_values(self, docids, data):

        data = data['data'][0]
        group_by = data['group_by']
        report_data = []
        report_groups = []
        domain = [('request_date', '>=', data['date_from']),
                  ('request_date', '<=', data['date_to']),
                  ('type', '=', data['purpose']),
                  ('employee_id', 'in', data['employee_ids']),
                  ('department_id', 'in', data['department_ids']),
                  ('requisition_type', '=', data['requisition_type'])]
        if data['purpose'] != 'service':
            domain.append(('location_id', '=', data['location_id'][0]), )
        requests = self.env['exchange.request'].search(domain)
        if data['type'] != 'total':
            requests = self.env['exchange.request.line'].search(
                [('exchange_id', 'in', requests.ids), ('product_id', 'in', data['product_ids'])])
        if not requests:
            raise ValidationError(_("There is no data"))
        if data['group_by'] == 'employee_id':
            report_groups = self.env['hr.employee'].browse(data['employee_ids'])
        else:
            report_groups = self.env['hr.department'].browse(data['department_ids'])

        docargs = {
            'doc_ids': [],
            'doc_model': ['exchange.request'],
            'docs': requests,
            'date_from': data['date_from'],
            'date_to': data['date_to'],
            'location_id': data['purpose'] != 'service' and data['location_id'][1],
            'company': self.env.user.company_id,
            'type': data['type'],
            'group_by': group_by,
            'report_groups': report_groups,
            'category': data['category_id'] and data['category_id'][1],
            'purpose': data['purpose'],
            'requisition_type': data['requisition_type']
        }
        return docargs
