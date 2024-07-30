# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
from dateutil import relativedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError, AccessError, UserError


class ExchangeRequestReport(models.AbstractModel):
    _name = "report.stock_custom_reports.inventory_adjustment_report"

    @api.model
    def _get_report_values(self, docids, data=None):

        data = data['data'][0]
        report_data = []
        report_groups = []
        domain = [('date', '>=', data['date_from']),
                  ('date', '<=', data['date_to']),
                      # ('filter', '=', data['filter']),
                  ('state', '=', data['state'])]
        # if data['filter'] == 'category':
        #     domain.append(('category_id', '=', data['category_id'][0]))
        if data['filter'] == 'product':
            domain.append(('product_id', 'in', data['product_ids']))

        inventory_records = self.env['stock.inventory'].search(domain)
        if not inventory_records:
            raise ValidationError(_("There is no data"))
        docargs = {
            'doc_ids': [],
            'doc_model': ['stock.inventory'],
            'docs': inventory_records,
            'date_from': data['date_from'],
            'date_to': data['date_to'],
            'location_id': data['location_id'][1],
            'company': self.env.user.company_id,
            'category': data['category_id'] and data['category_id'][1],
        }
        return docargs
