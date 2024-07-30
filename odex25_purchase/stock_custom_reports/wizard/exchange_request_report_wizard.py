# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from dateutil import relativedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError, AccessError, UserError

# Incoming Outgoing Report wizard
class ExchangeRequestReportWizard(models.TransientModel):
    _name = 'exchange.request.report'

    date_from = fields.Date(string='From',required=True,default=datetime.today())
    date_to = fields.Date(string='To',required=True,default=datetime.today())
    category_id = fields.Many2one('product.category',string="Category")
    product_ids = fields.Many2many('product.product',string='Products',)
    type = fields.Selection([('detailed' , 'Detailed'),('total' , 'Total')],string="Details")
    location_id = fields.Many2one('stock.location' , string='Location', domain=[('usage','=','internal')])
    purpose = fields.Selection(string='Purpose', selection=[('product', 'Product'), ('service', 'Service'),('gift' , 'Gift'),('custody' , 'Custody')])
    state = fields.Selection([
        ('draft','Draft'),
        ('direct_manager' , 'Department Manager'),
        ('confirm','Responsible Department'),
        ('sign','Sign'),
        ('waiting','Waiting For Purchase'),
        ('to_deliver','Waiting Delivery'),
        ('done','Done'),
        ('cancel','Cancel'),
    ],default='done')
    group_by = fields.Selection([('employee_id' , 'Employee') , ('department_id' , 'Department') ])
    employee_ids = fields.Many2many('hr.employee' , string="Employee")
    department_ids = fields.Many2many('hr.department' , string="Department")
    requisition_type = fields.Selection([('return' , 'Return'),('exchange','Exchange')])
    

    def print_report(self):
        form_values = self.read()
        if not form_values[0]['employee_ids']:
            form_values[0]['employee_ids'] = self.env['hr.employee'].search([]).ids
        if not form_values[0]['department_ids']:
            form_values[0]['department_ids'] = self.env['hr.department'].search([]).ids
        if not form_values[0]['product_ids']:
            form_values[0]['product_ids'] = self.env['product.product'].search([]).ids
        if self.date_to < self.date_from :
            raise exceptions.ValidationError(_("Date From Must Be Greater Than Date To"))
       
        
        datas = {
            'ids': [],
            'model': 'exchange.request',
            'data':form_values
            }
        return self.env.ref('stock_custom_reports.action_exchange_request_report').report_action(self, data=datas)

        
        
