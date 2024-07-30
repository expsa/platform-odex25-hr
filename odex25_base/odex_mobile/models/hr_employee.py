# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
import random
import json
import json, requests


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    device_id = fields.Char(string="Employee Device ")
    fcm_token = fields.Char(string='FCM Token')
    attendance_log_ids = fields.One2many('attendance.log','employee_id',string="Attendance Log")

    def user_push_notification(self, notification):
        url = "https://fcm.googleapis.com/fcm/send"
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'key=%s' % (self.env.user.company_id.fcm_server_key)
        }
        body = json.dumps({
            "to": self.fcm_token,
            "direct_boot_ok": True,
            "notification": notification
        })
        try:
            respons = requests.post(url=url, data=body, headers=header)
            return True
        except Exception as e:
            return False

    def create_employee_notification(self):
        emp_notif_obj = self.env['employee.notification']
        holiday_obj = self.env['hr.holidays']
        attendance_obj = self.env['attendance.attendance']

        employee_ids = self.env['hr.employee'].sudo().search([('state', '=', 'open')], order="id asc")
        date_now = datetime.utcnow()
        day_today = date_now.strftime('%A').lower()
        employee_list = []
        msg = ' '
        descrip_name = ''
        for emp in employee_ids:
            weekend_days = emp.resource_calendar_id.is_full_day and emp.resource_calendar_id.full_day_off or emp.resource_calendar_id.shift_day_off
            days_off = [day.name for day in weekend_days]
            if day_today not in days_off:
                min_sign_in = self.convert_float_2time(emp.resource_calendar_id.full_min_sign_in, date_now)
                max_sign_in = self.convert_float_2time(emp.resource_calendar_id.full_max_sign_in, date_now)
                min_sign_out = self.convert_float_2time(emp.resource_calendar_id.full_min_sign_out, date_now)
                max_sign_out = self.convert_float_2time(emp.resource_calendar_id.full_max_sign_out, date_now)

                holiday_ids = holiday_obj.search([('employee_id', '=', emp.id),('type', '!=', 'add'), 
                                                    ('date_from', '<=', str(date_now)),('date_to', '>=', str(date_now)), 
                                                    ('state', 'not in', ['draft', 'cancel', 'Refuse'])])
                
                attendance_in_ids = attendance_obj.search([('employee_id', '=', emp.id),('action', 'in', ['sign_in']), 
                                                    ('name', '>=', str(min_sign_in)), ('name', '<=', str(max_sign_in))])

                attendance_out_ids = attendance_obj.search([('employee_id', '=', emp.id),('action', 'in', ['sign_out']), 
                                                    ('name', '>=', str(min_sign_out)), ('name', '<=', str(max_sign_out))])

                if not holiday_ids:
                    if date_now >= min_sign_in and date_now <= max_sign_in and not attendance_in_ids:
                        employee_list.append(emp.id)
                        msg = _('Dear employee, Please Sign-in')
                        descrip_name = _(' Sign-in')
                    
                    if date_now >= min_sign_out and date_now <= max_sign_out and not attendance_out_ids:
                        employee_list.append(emp.id)
                        msg = _('Dear employee, Please Sign-out')
                        descrip_name = _(' Sign-out')

        if employee_list:
            notif_vals = {'name': _('Auto-Send for day ') + str(date_now.replace(microsecond=0)) + descrip_name, 'subject': _('attendances'), 'msg': msg,
                         'auto_send': True, 'employee_ids': [(6, 0, employee_list)]}
            notif_ids = emp_notif_obj.create(notif_vals)
            notif_ids.send()


    def convert_float_2time(self, time, date=None):
        hour, minute = divmod(time * 60, 60)

        return date.replace(hour=int(hour), minute=int(minute), second=0) - timedelta(hours=3)



class AttendanceLog(models.Model):
    _name = 'attendance.log'

    employee_id = fields.Many2one('hr.employee',string="Employee",)
    latitude = fields.Char(string="Latitude")
    longitude = fields.Char(string="Longitude")
    old = fields.Boolean(string="Old")
    active = fields.Boolean(string="Old",default=True)
    time = fields.Datetime()
    date = fields.Date()

class Attendance(models.Model):
    _inherit = 'attendance.attendance'

    action_type = fields.Selection(selection_add=[('system_checkout', 'Mobile System Force Checkout'),('application', 'Mobile Application'),('auto', 'Auto Checkout')])
    zone = fields.Char(string="Zone")
    latitude = fields.Char(string="Latitude")
    longitude = fields.Char(string="Longitude")


    def open_url(self):
        if self.latitude and self.longitude:
            url="https://www.google.com/maps/place/"+self.latitude+","+self.longitude
            return{'name': 'Go to Location',
             'res_model': 'ir.actions.act_url',
             'type': 'ir.actions.act_url',
             'target': 'self',
             'url': url
             }
        else:
            raise ValidationError(_("You can not open this location check latitude and longitude"))


class EmployeeNotification(models.Model):
    _name = 'employee.notification'

    name = fields.Char(string=" Name", required=True)
    general = fields.Boolean(string="General Zone")
    specific = fields.Boolean(string="Specific Zone")
    state = fields.Selection(string="State", selection=[('draft', 'Draft'),('send', 'Send')], default='draft')
    number = fields.Integer(string="Employee Number")
    subject = fields.Char(string="Subject")
    msg = fields.Text(string="Message")
    employee_ids = fields.Many2many('hr.employee', string="Employees")
    auto_send = fields.Boolean('Auto')

    @api.onchange('general', 'specific','number')
    def get_employees(self):
        for rec in self:
            rec.employee_ids = False
            domain = []
            emp_lst = False
            if not rec.general and not rec.specific:
                emp_lst = rec.env['hr.employee'].sudo().search([('state', '=', 'open')])
            else:
                if rec.general:
                    domain += [('general', '=', True)]
                if rec.specific:
                    domain += [('specific', '=', True)]
                emp_lst = self.env['attendance.zone'].sudo().search(domain).mapped('employee_ids')
            if emp_lst:
                if rec.number > len(emp_lst):
                    raise ValidationError(_("Number of Nominated employee greater than employee"))
                emp = random.sample(emp_lst.ids, rec.number)
                rec.employee_ids = emp if emp else False
            return {
                'domain': {'employee_ids': [('id', 'in', emp_lst.ids)]}
            }

    def send(self):
        for rec in self:
            if not rec.employee_ids:
                rec.get_employees()
            if rec.employee_ids:
                for emp in rec.employee_ids:
                    if emp.user_id.partner_id:
                        partner_id = emp.user_id.partner_id
                        msg = rec.msg
                        subject = rec.subject
                        value = {
                            'msg' : rec.msg,
                        'subject' : rec.subject,
                        }
                        data = {
                            'meta': json.dumps({
                                'type': 'notification',
                                'data': value
                            })}
                        partner_id.send_notification(
                            subject,msg,data=data, all_device=True)
                        emp.user_push_notification({
                            'title' : rec.msg,
                        'body' : rec.subject,
                        })
            else:
                raise  ValidationError(_("No employee Selected"))
            rec.state = 'send'

