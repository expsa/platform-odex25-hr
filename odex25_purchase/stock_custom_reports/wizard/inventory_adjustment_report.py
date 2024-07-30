# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from dateutil import relativedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError, AccessError, UserError

# Incoming Outgoing Report wizard
class InventoryAdjustmentReportWizard(models.TransientModel):
    _name = 'inventory.adjustment.report'

    date_from = fields.Date(string='From',required=True,default=datetime.today())
    date_to = fields.Date(string='To',required=True,default=datetime.today())
    category_id = fields.Many2one('product.category',string="Category")
    product_ids = fields.Many2many('product.product',string='Products',)
    type = fields.Selection([('detailed' , 'Detailed'),('total' , 'Total')],string="Details")
    location_id = fields.Many2one('stock.location' , string='Location', domain=[('usage','=','internal')])
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm' , 'Confirm'),
        ('done','Done'),
    ],default='done')

    filter = fields.Selection([
            ('none', _('All products')),
            ('category', _('One product category')),
            ('product', _('One product only'))],
        string='Inventory Type',
        required=True,
        default='none')
    
    

    def print_report(self):
        form_values = self.read()
        if self.date_to < self.date_from :
            raise exceptions.ValidationError(_("Date From Must Be Greater Than Date To"))
       
        
        datas = {
            'ids': [],
            'model': 'stock.inventory',
            'data':form_values
            }
        return self.env.ref('stock_custom_reports.action_inventory_adjustment_report').report_action(self, data=datas)

        
        
