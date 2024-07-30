# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
from dateutil import relativedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError, AccessError, UserError


class StockMoveCustom(models.Model):
    _inherit = 'stock.move.line'

    partner_id = fields.Many2one('res.partner', related="move_id.picking_id.partner_id", store=True)


class IncomingOutgoingReport(models.AbstractModel):
    _name = "report.stock_custom_reports.scrap_report"

    @api.model
    def _get_report_values(self, docids, data):
        data = data['data'][0]

        domain = [('date_expected', '>=', data['date_from']), ('date_expected', '<=', data['date_to']),
                  ('state', '=', 'done')]
        if data['product_ids']:
            domain.append(('product_id', 'in', data['product_ids']))
        if data['location_id']:
            domain.append(('location_id', 'in', [data['location_id'][0]]))
        moves = self.env['stock.scrap'].search(domain)
        if not moves:
            raise ValidationError(_("There is no data"))
        docargs = {
            'doc_ids': [],
            'doc_model': ['stock.scrap'],
            'docs': self.env['stock.scrap'].browse(moves.ids),
            'date_from': data['date_from'],
            'date_to': data['date_to'],
            'location_id': data.get('location_id', False) and data.get('location_id', False)[1],
            'company': self.env.user.company_id,
            'category': data['category_id'] and data['category_id'][1]
        }
        return docargs
