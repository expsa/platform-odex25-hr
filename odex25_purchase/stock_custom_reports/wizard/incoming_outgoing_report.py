# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from dateutil import relativedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError, AccessError, UserError

# Incoming Outgoing Report wizard
class IncomingOutgoingReportWizard(models.TransientModel):
    _name = 'incoming.outgoing.report'

    date_from = fields.Date(string='From',required=True,default=datetime.today())
    date_to = fields.Date(string='To',required=True,default=datetime.today())
    location_id = fields.Many2one('stock.location' , string='Location', domain=[('usage','=','internal')])
    category_id = fields.Many2one('product.category',string="Category")
    product_ids = fields.Many2many('product.product','incoming_outgoing_products_rel','wizard_id','product_id' ,string='Products',)
    with_prices = fields.Boolean('With Prices')
    type = fields.Selection(string='Type', selection=[('income', 'Incomming'), ('out', 'Out going'),])
    detailing = fields.Selection([('detailed' , 'Detailed'),('total' , 'Total')],string="Details")
    group_by = fields.Selection([('product_id' , 'Product') , ('picking_id' , 'Shipment'),('partner_id' , 'Partner') ])
    partner_ids = fields.Many2many('res.partner' , string="Partner")
    
    

    def print_report(self):
        print('innnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
        form_values = self.read()
        if self.date_to < self.date_from :
            raise exceptions.ValidationError(_("Date From Must Be Greater Than Date To"))
       
        
        datas = {
            'ids': [],
            'model': 'stock.move.line',
            'data':form_values
            }
        if self.detailing == "total":
            # if self.with_prices:
            # return self.env.ref('stock_custom_reports.action_incoming_outgoing_with_price_report').report_action(self, data=datas)
            return self.env.ref('stock_custom_reports.action_incoming_outgoing_report').report_action(self, data=datas)
        else:
            print('immmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
            return self.env.ref('stock_custom_reports.action_incoming_outgoing_detailed_report').report_action(self, data=datas)

        
        
