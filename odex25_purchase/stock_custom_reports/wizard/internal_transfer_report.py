# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from dateutil import relativedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError, AccessError, UserError

# Incoming Outgoing Report wizard
class InternalTransferReportWizard(models.TransientModel):
    _name = 'internal.transfer.report'

    date_from = fields.Date(string='From',required=True,default=datetime.today())
    date_to = fields.Date(string='To',required=True,default=datetime.today())
    category_id = fields.Many2one('product.category',string="Category")
    product_ids = fields.Many2many('product.product',string='Products',)
    type = fields.Selection([('detailed' , 'Detailed'),('total' , 'Total')],string="Details")
    operation_type = fields.Selection([('location_dest_id' , 'Incomming'),('location_id' , 'Outgoing')],string="Operation Type")
    location_id = fields.Many2one('stock.location' , string='Location', domain=[('usage','=','internal')])
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],string='State',help='Leave it Empty for all states',default="done")    
    
    

    def print_report(self):
        form_values = self.read()
        if self.date_to < self.date_from :
            raise exceptions.ValidationError(_("Date From Must Be Greater Than Date To"))
        if not form_values[0]['product_ids']:
            form_values[0]['product_ids'] = self.env['product.product'].search([]).ids
       
        
        datas = {
            'ids': [],
            'model': 'stock.inventory',
            'data':form_values
            }
        return self.env.ref('stock_custom_reports.action_internal_transfer_report').report_action(self, data=datas)

        
        
