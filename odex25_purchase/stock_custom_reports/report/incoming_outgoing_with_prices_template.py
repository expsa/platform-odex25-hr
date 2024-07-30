# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
from dateutil import relativedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError, AccessError, UserError



class StockMoveCustom(models.Model):
    _inherit = 'stock.move.line'

    partner_id =  fields.Many2one('res.partner' , related="move_id.picking_id.partner_id",store=True)



class IncomingOutgoingReport(models.AbstractModel):
    _name="report.stock_custom_reports.incoming_outgoing_detailed_report"



    @api.model
    def _get_report_values(self,docids, data):
        data = data['data'][0]
        group_by = data['group_by']
        report_data = []
        domain = [('date' , '>=' , data['date_from']),('date' , '<=' , data['date_to'])]
        if data['partner_ids']:
            domain.append(('partner_id' , 'in' , data['partner_ids']))
        if data['product_ids']:
            domain.append(('product_id' , 'in' , data['product_ids']))
        if data['type'] == 'income':
            domain.append(('location_dest_id' , 'in' , [data['location_id'][0]]))
        else:
            domain.append(('location_id' , 'in' , [data['location_id'][0]]))
        moves = self.env['stock.move.line'].read_group(domain,groupby=[group_by],fields=[group_by])
        for group in moves:
            if not group[group_by]:
                continue
            report_data.append({
                'lable' : group[group_by] and group[group_by][1],
                'data' : self.env['stock.move.line'].browse(self.env['stock.move.line'].search(group['__domain']).ids)
            })

        docargs={
                'doc_ids':[],
                'doc_model':['stock.move.line'],
                'docs': report_data,	
                'date_from':data['date_from'],
                'date_to':data['date_to'],
                'location_id': data['location_id'][1],
                'company':self.env.user.company_id,
                'type' : data['type'],
                'group_by' : group_by,
                'category' :  data['category_id'] and data['category_id'][1]
                    }
        return docargs



