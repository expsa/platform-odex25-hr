# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from dateutil import relativedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError, AccessError, UserError

# Incoming Outgoing Report wizard
class ScrapReportWizard(models.TransientModel):
    _name = 'scrap.report.wizard'

    date_from = fields.Date(string='From',required=True,default=datetime.today())
    date_to = fields.Date(string='To',required=True,default=datetime.today())
    category_id = fields.Many2one('product.category',string="Category")
    product_ids = fields.Many2many('product.product',string='Products',)
    location_id = fields.Many2one('stock.location' , string='Location', domain=[('usage','=','internal')])
    
    

    def print_report(self):
        form_values = self.read()
        if self.date_to < self.date_from :
            raise exceptions.ValidationError(_("Date From Must Be Greater Than Date To"))
       
        
        datas = {
            'ids': [],
            'model': 'exchange.request',
            'data':form_values
            }
        return self.env.ref('stock_custom_reports.action_scrap_report').report_action(self, data=datas)

        
        
