# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
from dateutil import relativedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError, AccessError, UserError


class InternalTransferReport(models.AbstractModel):
    _name = "report.stock_custom_reports.internal_transfer_report"

    @api.model
    def _get_report_values(self, docids, data):

        data = data['data'][0]
        report_data = []
        report_groups = []
        stock_operations = self.env['stock.picking.type'].search([('code', '=', 'internal')]).ids
        domain = [('scheduled_date', '>=', data['date_from']),
                  ('scheduled_date', '<=', data['date_to']),
                  (data['operation_type'], '=', data['location_id'][0]),
                  ('picking_type_id', 'in', stock_operations)]
        if data['state']:
            domain.append(('state', '=', data['state']))
        report_records = self.env['stock.picking'].search(domain)
        if data['type'] != 'total':
            report_records = self.env['stock.move'].search(
                [('picking_id', 'in', report_records.ids), ('product_id', 'in', data['product_ids'])])
        if not report_records:
            raise ValidationError(_("There is no data"))

        docargs = {
            'doc_ids': [],
            'doc_model': [report_records[0]._name],
            'docs': report_records,
            'date_from': data['date_from'],
            'date_to': data['date_to'],
            'location_id': data['location_id'][1],
            'company': self.env.user.company_id,
            'type': data['type'],
            'category': data['category_id'] and data['category_id'][1],
            'operation_type': data['operation_type']
        }
        return docargs
