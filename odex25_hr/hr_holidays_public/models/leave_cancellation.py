# -*- coding: utf-8 -*-
from datetime import datetime as dt
from datetime import timedelta

from odoo import models, fields, api, exceptions
from odoo.tools.translate import _


class LeaveCancellation(models.Model):
    _name = 'leave.cancellation'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    state = fields.Selection(selection=[("draft", _("Draft")),
                                        ("submit", _("Submit")),
                                        ("review", _("Direct Manager")),
                                        ("confirm", _("HR Manager")),
                                        ("approve", _("Approved")),
                                        ("refuse", _("Refused"))
                                        ], default='draft',tracking=True)
    from_hr_department = fields.Boolean()
    # employee_id = fields.Many2one(comodel_name='hr.employee')
    job_id = fields.Many2one(related='employee_id.job_id', readonly=True)
    department_id = fields.Many2one(related='employee_id.department_id', readonly=True)
    leave_cancellation_date = fields.Datetime()
    cause = fields.Char()
    from_date = fields.Datetime()
    leave_request_id = fields.Many2one(comodel_name='hr.holidays', store=True ,force_save=True)
    leave_date_from = fields.Datetime(related='leave_request_id.date_from', store=True)
    leave_date_to = fields.Datetime(related='leave_request_id.date_to', store=True)
    attachment_ids = fields.One2many('ir.attachment', 'leave_cancel_id')
    employee_id = fields.Many2one('hr.employee', 'Employee', default=lambda item: item.get_user_id())
    duration_canceled = fields.Float(force_save=1)
    salary_rule_id = fields.Many2one('hr.salary.rule', string='Benefits/Discounts')
    reconcile_leave = fields.Boolean(related='leave_request_id.reconcile_leave')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    def get_user_id(self):
        employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        if employee_id:
            return employee_id.id
        else:
            return False

    @api.onchange('leave_request_id')
    def onchange_leave(self):
        self.duration_canceled = 0
        self.from_date = False
        self.leave_cancellation_date = False

    @api.onchange('from_date', 'leave_cancellation_date', 'leave_date_from')
    def onchange_dates(self):
        for leave_req in self:
            if self.from_date and self.leave_cancellation_date:
                if leave_req.leave_request_id.date_to:
                    if leave_req.leave_request_id.date_from:
                        leave_cancel_1 = dt.strptime(str(leave_req.leave_cancellation_date),
                                                     "%Y-%m-%d %H:%M:%S").date()
                        leave_from_1 = dt.strptime(str(leave_req.from_date), "%Y-%m-%d %H:%M:%S").date()
                        leave_date_to_value = dt.strptime(str(leave_req.leave_request_id.date_to),
                                                          "%Y-%m-%d %H:%M:%S").date()
                        leave_date_from_value = dt.strptime(str(leave_req.leave_request_id.date_from),
                                                            "%Y-%m-%d %H:%M:%S").date()
                        if leave_cancel_1 < leave_from_1:
                            raise exceptions.Warning(
                                _('Leave cancellation Date To field must be greater than date from field'))
                        if leave_from_1 < leave_date_from_value or leave_cancel_1 > leave_date_to_value:
                            raise exceptions.Warning(
                                _('Duration of leave cancel must be between duration of request of leave '))
                        else:
                            leave_req.duration_canceled = (leave_cancel_1 - leave_from_1).days + 1
            else:
                leave_req.duration_canceled = 0

    @api.onchange('employee_id')
    def _get_leaves_related_date(self):
        for item in self:
            leaves_ids = self.env['hr.holidays'].search(
                [('employee_id', '=', item.employee_id.id), ('state', '=', 'validate1'), ('type', '=', 'remove')]).ids
            if leaves_ids:
                return {'domain': {'leave_request_id': [('id', 'in', leaves_ids)]}}
            else:
                return {'domain': {'leave_request_id': [('id', 'in', [])]}}

    def draft(self):
        for item in self:
            balance = self.env['hr.holidays'].search([('employee_id', '=', item.employee_id.id),
                                                      ('holiday_status_id', '=',
                                                       item.leave_request_id.holiday_status_id.id),
                                                      ('type', '=', 'add'),
                                                      ('check_allocation_view', '=', 'balance')])

            if balance and item.leave_request_id.canceled_duration > 0:
                cancelled_days = self.get_pure_holiday_days()
                var_remaining_leaves = balance.remaining_leaves - cancelled_days
                var_taken_leaves = balance.leaves_taken + cancelled_days
                item.leave_request_id.number_of_days_temp = item.leave_request_id.number_of_days_temp + cancelled_days
                item.leave_request_id.canceled_duration = \
                    item.leave_request_id.canceled_duration > item.duration_canceled and \
                    item.leave_request_id.canceled_duration - item.duration_canceled or \
                    0.0
                balance.write({
                    'remaining_leaves': var_remaining_leaves,
                    'leaves_taken': var_taken_leaves,
                    # 'number_of_days_temp': var_remaining_leaves,
                    # 'virtual_remaining_leaves': var_remaining_leaves,
                })
        self.state = 'draft'

    def submit(self):
        for item in self:
            if item.leave_request_id.return_from_leave:
                raise exceptions.Warning(_("You can't cancel or cut request holiday after return from"))
        self.state = 'submit'

    def review(self):
        self.state = 'review'

    def confirm(self):
        self.state = 'confirm'

    def get_pure_holiday_days(self):
        for item in self:
            cancellation_dates = []
            from_dt = dt.strptime(str(item.from_date), "%Y-%m-%d %H:%M:%S")
            for i in range((dt.strptime(str(item.leave_cancellation_date), "%Y-%m-%d %H:%M:%S") - from_dt).days + 1):
                cancellation_dates.append(from_dt.date() + timedelta(days=i))
            cancelled_days = list(set(cancellation_dates))

            if item.leave_request_id.holiday_status_id.official_holidays is False:
                event_dates = []
                for event in self.env['hr.holiday.officials'].search([('active', '=', True), ('state', '=', 'confirm'),
                                                                      ('date_from', '<=', item.leave_cancellation_date),
                                                                      ('date_to', '>=', item.from_date)]):
                    if event.religion and item.employee_id and item.employee_id.religion != event.religion:
                        continue
                    event_df = dt.strptime(str(event.date_from), '%Y-%m-%d').date()
                    dlt = dt.strptime(str(event.date_to), '%Y-%m-%d').date() - event_df
                    for i in range(dlt.days + 1):
                        event_dates.append(event_df + timedelta(days=i))
                cancelled_days = list(set(cancellation_dates) - set(event_dates))

            if item.leave_request_id.holiday_status_id.working_days:
                days_off = [d.name.title() for d in item.employee_id.resource_calendar_id and
                            (item.employee_id.resource_calendar_id.full_day_off or
                             item.employee_id.resource_calendar_id.shift_day_off) or
                            item.employee_id.company_id.resource_calendar_id and
                            (item.employee_id.company_id.resource_calendar_id.full_day_off or
                             item.employee_id.company_id.resource_calendar_id.shift_day_off)]
                for cnl in cancelled_days:
                    if cnl.strftime('%A') in days_off:
                        cancelled_days.remove(cnl)
        return len(cancelled_days)

    def approve(self):
        for item in self:
            balance = self.env['hr.holidays'].search([('employee_id', '=', item.employee_id.id),
                                                      ('holiday_status_id', '=',
                                                       item.leave_request_id.holiday_status_id.id),
                                                      ('type', '=', 'add'),
                                                      ('check_allocation_view', '=', 'balance')])
            if balance:
                cancelled_days = self.get_pure_holiday_days()
                var_remaining_leaves = balance.remaining_leaves + cancelled_days
                var_taken_leaves = balance.leaves_taken - cancelled_days

                item.leave_request_id.number_of_days_temp = item.leave_request_id.number_of_days_temp - cancelled_days
                item.leave_request_id.canceled_duration =\
                    item.leave_request_id.canceled_duration > 0 and \
                    item.leave_request_id.canceled_duration + cancelled_days or \
                    cancelled_days
                balance.write({
                    'remaining_leaves': var_remaining_leaves,
                    'leaves_taken': var_taken_leaves,
                    # 'number_of_days_temp': var_remaining_leaves,
                    # 'virtual_remaining_leaves': var_remaining_leaves,
                })
            reconcile_leave_id = self.env['reconcile.leaves'].search([
                ('yearly_vacation', '=', item.leave_request_id.id),
                ('state', '=', 'pay'),
            ])
            if item.leave_request_id.reconcile_leave:
                if not reconcile_leave_id:
                    raise exceptions.Warning(_('Kindly, process the reconciliation of leave'
                                               ' before process cancel leave'))
                date_start = dt.strptime(str(item.from_date), "%Y-%m-%d %H:%M:%S")
                date_end = dt.strptime(str(item.leave_cancellation_date), "%Y-%m-%d %H:%M:%S")
                cancel_leave_duration = int((date_end - date_start).days) + 1
                self.env['contract.advantage'].create({
                    "employee_id": item.employee_id.id,
                    "contract_advantage_id": self.employee_id.contract_id and self.employee_id.contract_id.id or False,
                    "type": "exception",
                    "date_from": item.from_date,
                    "date_to": item.leave_cancellation_date,
                    "amount": reconcile_leave_id.salary / (30 / cancel_leave_duration),
                    "benefits_discounts": item.salary_rule_id and item.salary_rule_id.id or False,
                })

            item.state = 'approve'

    def refuse(self):
        self.state = 'refuse'

    def unlink(self):
        for i in self:
            if i.state != 'draft':
                raise exceptions.Warning(_('You can not delete record in state not in draft'))
        return super(LeaveCancellation, self).unlink()


class Attachment(models.Model):
    _inherit = 'ir.attachment'

    leave_cancel_id = fields.Many2one(comodel_name='leave.cancellation')
