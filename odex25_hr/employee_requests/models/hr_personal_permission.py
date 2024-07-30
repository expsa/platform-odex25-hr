# -*- coding: utf-8 -*-

from calendar import monthrange
import time
from datetime import datetime
from odoo import models, fields, api, _, exceptions
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import timedelta
from odoo.exceptions import ValidationError


class HrPersonalPermission(models.Model):
    _name = 'hr.personal.permission'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    from_hr_department = fields.Boolean()
    date = fields.Date(default=lambda self: fields.Date.today())
    date_from = fields.Datetime()
    date_to = fields.Datetime()
    duration = fields.Float(compute='get_duration_no' ,store=True)
    employee_contract_id = fields.Many2one(comodel_name='hr.contract.type')
    balance = fields.Float(related='employee_id.contract_id.working_hours.permission_hours')

    permission_number = fields.Float(force_save=True, readonly=True, store=True,
                                     help='The Remaining Number of Hours permission This Month')
    early_exit = fields.Boolean()
    mission_purpose = fields.Text()

    employee_no = fields.Char(related='employee_id.emp_no', readonly=True)
    job_id = fields.Many2one(related='employee_id.job_id', readonly=True)
    department_id = fields.Many2one(related='employee_id.department_id', readonly=True)
    refuse_cause = fields.Text()
    attach_ids = fields.One2many('ir.attachment', 'personal_permission_id')
    approved_by = fields.Many2one(comodel_name='res.users')
    refused_by = fields.Many2one(comodel_name='res.users')
    employee_id = fields.Many2one('hr.employee', 'Employee Id', default=lambda item: item.get_user_id(),
                                  domain=[('state', '=', 'open')])

    state = fields.Selection(
        [('draft', _('Draft')), ('send', _('Send')), ('direct_manager', _('Direct Manager')),
         ('approve', _('approve'))
            , ('refused', _('Refused'))], default="draft", tracking=True)

    type_exit = fields.Selection(
        [('early_exit', _('Early Exit')), ('late entry', _('Late Entry')), ('during work', _('During Work'))],
        default="early_exit")

    company_id = fields.Many2one('res.company',string="Company", default=lambda self: self.env.user.company_id)

    @api.model
    def create(self, vals):
        new_record = super(HrPersonalPermission, self).create(vals)
        for item in new_record:
            if item.date_from and item.date_to and item.employee_id:
                calendar = item.employee_id.resource_calendar_id
                start_date = datetime.strptime(str(item.date_to), "%Y-%m-%d %H:%M:%S")
                end_date = datetime.strptime(str(item.date_to), "%Y-%m-%d %H:%M:%S")
                hour_star = start_date.hour + 3
                hour_end = end_date.hour + 3

                if calendar.is_full_day:
                    cal_hour_star = calendar.full_min_sign_in
                    cal_hour_end = calendar.full_max_sign_out
                    if cal_hour_end <= hour_end or hour_end < cal_hour_star:
                        raise exceptions.Warning(_('Sorry, Permission Must Be within The Attendance Hours'))

        return new_record

    @api.onchange('date_from')
    def _get_duration_hours(self):
        for item in self:
            if item.date_from:
                permission_hour = item.employee_id.resource_calendar_id.permission_hours
                start_date_hour = datetime.strptime(str(item.date_from), "%Y-%m-%d %H:%M:%S")
                end_date_hour = start_date_hour + timedelta(hours=permission_hour)
                item.date_to = end_date_hour

    @api.depends('date_from', 'date_to')
    def get_duration_no(self):
        for item in self:
            if item.date_from and item.date_to:
                start_date_value = datetime.strptime(str(item.date_from), "%Y-%m-%d %H:%M:%S")
                end_date = datetime.strptime(str(item.date_to), "%Y-%m-%d %H:%M:%S")
                if start_date_value <= end_date:
                    days = (end_date - start_date_value).days
                    seconds_diff = (end_date - start_date_value).seconds
                    item.duration = (days * 24) + seconds_diff / 3600

    #  function permission_number_decrement and _get_date_constrains replaced in new module hr permission holiday to fix
    #  singleton issue and change constrain

    @api.onchange('date_to', 'date_from', 'employee_id')
    def permission_number_decrement(self):
        for item in self:
            if item.employee_id:
                if not item.employee_id.first_hiring_date:
                    raise exceptions.Warning(
                        _('You can not Request Permission The Employee have Not First Hiring Date'))
            if item.date_to:
                current_date = datetime.strptime(str(item.date_to), DEFAULT_SERVER_DATETIME_FORMAT)
                current_month = datetime.strptime(str(item.date_to), DEFAULT_SERVER_DATETIME_FORMAT).month
                date_from = current_date.strftime('%Y-{0}-01'.format(current_month))
                date_to = current_date.strftime('%Y-{0}-01'.format(current_month + 1))
                if current_month == 12:
                    date_to = current_date.strftime('%Y-{0}-31'.format(current_month))
                number_of_per = item.employee_id.contract_id.working_hours.permission_number
                employee_permissions = self.search([
                    ('employee_id', '=', item.employee_id.id),
                    ('state', '=', 'approve'),
                    ('date_from', '>=', date_from),
                    ('date_to', '<=', date_to)])

                all_perission = 0
                for rec in employee_permissions:
                    all_perission += rec.duration

                    if rec.date_to and item.date_to:
                        permission_date1 = datetime.strptime(rec.date_to,
                                                             DEFAULT_SERVER_DATETIME_FORMAT).date()
                        date_to_value1 = datetime.strptime(item.date_to, DEFAULT_SERVER_DATETIME_FORMAT).date()

                        if permission_date1 == date_to_value1:
                            raise exceptions.Warning(
                                _('Sorry You Have Used All Your Permission In This Day you have one permission per a Day'))


                if number_of_per > all_perission:

                    item.permission_number = round(number_of_per - all_perission, 2)
                else:

                    raise ValidationError(_('Sorry You Have Used All Your Permission Hours In This Month'))

    def check_holiday_mission(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                clause_1, clause_2, clause_3 = rec.get_domain(rec.date_from, rec.date_to)
                clause_final = [('id', '!=', rec.id), ('employee_id', '=', rec.employee_id.id),
                                ('state', '!=', 'refuse'),
                                '|', '|'] + clause_1 + clause_2 + clause_3
                record = rec.search(clause_final)
                if record:
                    raise exceptions.Warning(_('Sorry The Employee Actually in Permission For this Period'))
                Module = self.env['ir.module.module'].sudo()
                modules = Module.search([('state', '=', 'installed'), ('name', '=', 'exp_official_mission')])
                modules_holidays = Module.search([('state', '=', 'installed'), ('name', '=', 'hr_holidays_public')])
                date_to = str(datetime.strptime(str(rec.date_to), DEFAULT_SERVER_DATETIME_FORMAT).date())
                date_from = str(datetime.strptime(str(rec.date_from), DEFAULT_SERVER_DATETIME_FORMAT).date())
                clause_1, clause_2, clause_3 = rec.get_domain(date_from, date_to)
                if modules_holidays:
                    clause_final = [('employee_id', '=', rec.employee_id.id), ('state', '!=', 'refuse'),
                                    ('type', '=', 'remove'),
                                    '|', '|'] + clause_1 + clause_2 + clause_3
                    holidays = self.env['hr.holidays'].search(clause_final)
                    if holidays:
                        raise exceptions.Warning(_('Sorry The Employee %s Actually On %s For this Period') %
                                                 (rec.employee_id.name, holidays.holiday_status_id.name))
                if modules:
                    date_to = datetime.strptime(str(self.date_to), DEFAULT_SERVER_DATETIME_FORMAT)
                    date_from = datetime.strptime(str(self.date_from), DEFAULT_SERVER_DATETIME_FORMAT)
                    if date_to and date_from:
                        delta = timedelta(days=1)
                        while date_from <= date_to:
                            clause_1, clause_2, clause_3 = self.get_mission_domain(date_from, date_from)
                            clause_final = [('employee_id', '=', rec.employee_id.id),
                                            ('official_mission_id.state', '!=', 'refused'),
                                            ('date_from', '<=', str(date_from.date())),
                                            ('date_to', '>=', str(date_from.date())),
                                            '|', '|'] + clause_1 + clause_2 + clause_3
                            mission_dfrm = self.env['hr.official.mission.employee'].search(clause_final)
                            if mission_dfrm:
                                raise exceptions.Warning(_('Sorry The Employee %s Actually'
                                                           ' On Mission/Training For this Period') % rec.employee_id.name)
                            date_from += delta

    def get_mission_domain(self, date_from, date_to):
        date_from_time = (date_from + timedelta(hours=3)).time()
        date_to_time = (date_to + timedelta(hours=3)).time()
        hour_from = date_from_time.hour + date_from_time.minute / 60.0
        hour_to = date_to_time.hour + date_to_time.minute / 60.0
        clause_1 = ['&', ('hour_from', '<=', hour_from), ('hour_to', '>=', hour_from)]
        clause_2 = ['&', ('hour_from', '<=', hour_to), ('hour_to', '>=', hour_to)]
        clause_3 = ['&', ('hour_from', '>=', hour_from), ('hour_to', '<=', hour_to)]
        return clause_1, clause_2, clause_3

    def get_domain(self, date_from, date_to):
        clause_1 = ['&', ('date_to', '<=', date_to), ('date_to', '>=', date_from)]
        clause_2 = ['&', ('date_from', '<=', date_to), ('date_from', '>=', date_from)]
        clause_3 = ['&', ('date_from', '<=', date_from), ('date_to', '>=', date_to)]
        return clause_1, clause_2, clause_3

    @api.constrains('date_from', 'date_to')
    def _get_date_constrains(self):
        for item in self:
            item.check_holiday_mission()
            current_month = (datetime.utcnow() + timedelta(hours=3)).date().month
            current_year = (datetime.utcnow() + timedelta(hours=3)).date().year
            month_len = monthrange(current_year, current_month)[1]
            number_of_per = item.employee_id.contract_id.working_hours.permission_number
            number_of_durations = item.employee_id.contract_id.working_hours.permission_hours
            this_month_permission = self.search([('employee_id', '=', item.employee_id.id), ('state', '=', 'approve'),
                                                 ('date_from', '>=', time.strftime('%Y-{0}-1'.format(current_month))),
                                                 ('date_to', '<=',
                                                  time.strftime('%Y-{0}-{1}'.format(current_month, month_len)))])
            if item.date_to:
                current_date = datetime.strptime(str(item.date_to), DEFAULT_SERVER_DATETIME_FORMAT)
                current_month = datetime.strptime(str(item.date_to), DEFAULT_SERVER_DATETIME_FORMAT).month
                date_from = current_date.strftime('%Y-{0}-01'.format(current_month))
                date_to = current_date.strftime('%Y-{0}-01'.format(current_month + 1))
                if current_month == 12:
                    date_to = current_date.strftime('%Y-{0}-31'.format(current_month))
                employee_permissions = self.search([
                    ('employee_id', '=', item.employee_id.id),
                    ('state', '=', 'approve'),
                    ('date_from', '>=', date_from),
                    ('date_to', '<=', date_to)])

            all_perission = 0
            for rec in employee_permissions:
                all_perission += rec.duration

            if number_of_per < all_perission:
                raise ValidationError(_('Sorry You Have Used All Your Permission Hours In This Month'))

            start_date_value = datetime.strptime(str(item.date_from), "%Y-%m-%d %H:%M:%S")
            end_date = datetime.strptime(str(item.date_to), "%Y-%m-%d %H:%M:%S")
            if start_date_value <= end_date:
                days = (end_date - start_date_value).days
                seconds_diff = (end_date - start_date_value).seconds
                item.duration = (days * 24) + seconds_diff / 3600
                if item.duration <= 0.0:
                    raise exceptions.Warning(_('This Duration Must Be Greater Than Zero'))

                if item.duration < item.balance:
                    raise exceptions.Warning(_('This Duration must be less than or equal to the Permission Limit'))

                if item.duration > item.permission_number:
                    raise exceptions.Warning(
                        _('This Duration not Allowed it must be Less Than or equal Permission Hours in Month'))

                if employee_permissions.date_to and item.date_to:
                    permission_date = datetime.strptime(str(employee_permissions.date_to),
                                                        DEFAULT_SERVER_DATETIME_FORMAT).date()
                    date_to_value = datetime.strptime(str(item.date_to), DEFAULT_SERVER_DATETIME_FORMAT).date()

                    if permission_date == date_to_value:
                        raise exceptions.Warning(
                            _('Sorry You Have Used All Your Permission In This Day you have one permission per a Day'))
            else:
                raise exceptions.Warning(_('End Date must be greater than Start Date'))

    @api.constrains('date_from', 'date_to')
    def _get_date_constrains2(self):
        for item in self:
            start_date_value = datetime.strptime(str(item.date_from), "%Y-%m-%d %H:%M:%S")
            end_date = datetime.strptime(str(item.date_to), "%Y-%m-%d %H:%M:%S")
            if start_date_value > end_date:
                raise exceptions.Warning(_('End Date must be greater than Start Date'))

    def draft_state(self):
        self.state = "draft"
        self.call_cron_function()

    def call_cron_function(self):
        date = datetime.strptime(str(self.date), "%Y-%m-%d")
        self.env['hr.attendance.transaction'].process_attendance_scheduler_queue(date, self.employee_id)

    # @api.constrains('date_from', 'date_to')
    def send(self):
        self._get_date_constrains2()
        self.state = "send"

    def direct_manager(self):
        self.state = "direct_manager"

    def approve(self):
        self.state = "approve"
        self.call_cron_function()

    def refused(self):
        self.state = "refused"

    def get_user_id(self):
        employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        if employee_id:
            return employee_id.id
        else:
            return False

    def unlink(self):
        for i in self:
            if i.state != 'draft':
                raise exceptions.Warning(_('You can not delete record in state not in draft'))
        return super(HrPersonalPermission, self).unlink()


class HrPersonalPermissionAttach(models.Model):
    _inherit = 'ir.attachment'

    personal_permission_id = fields.Many2one(comodel_name='hr.personal.permission')
