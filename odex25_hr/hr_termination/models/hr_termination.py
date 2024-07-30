# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError, UserError
from datetime import date, timedelta, datetime as dt
from dateutil import relativedelta
import logging
from num2words import num2words
from hijri_converter import convert
import math

_logger = logging.getLogger(__name__)

date_format = "%Y-%m-%d"


class HrTermination(models.Model):
    _name = 'hr.termination'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'
    _description = 'Termination'

    # default compute function
    def _get_employee_id(self):
        # assigning the related employee of the logged in user
        employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        return employee_rec.id

    name = fields.Char(string='Order Reference', copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    joined_date = fields.Date(string="Join Date", help='Joining date of the employee')
    resign_confirm_date = fields.Date(string="Termination confirm date", help='Date on which the request is confirmed')
    approved_revealing_date = fields.Date(string="Approved Date", help='The date approved for the revealing')
    term_reason = fields.Text(string="Reason", help='Specify reason for leaving the company')
    notice_period = fields.Char(string="Notice Period", compute='_notice_period')
    contract_start_date = fields.Date(related='contract_id.date_start')
    contract_end_date = fields.Date(related='contract_id.date_end')
    salary = fields.Float(related='contract_id.total_allowance')
    first_hire_date = fields.Date(related='employee_id.first_hiring_date')
    last_work_date = fields.Date(tracking=True)
    salary_date_from = fields.Date(store=True, force_save=True, help='Calculate The Last Salary Date From')
    salary_date_to = fields.Date(store=True, force_save=True, help='Calculate The Last Salary Date To')
    paid_duration = fields.Float(compute='_get_paid_duration')
    salary_for_eos = fields.Float()
    service_year = fields.Integer()
    service_month = fields.Integer()
    service_day = fields.Integer()
    reason = fields.Text()
    unpaid_year = fields.Integer()
    unpaid_month = fields.Integer()
    unpaid_day = fields.Integer()
    reason = fields.Text()
    remaining_accommodation = fields.Float()
    salary_amount = fields.Float()
    deduction_balance = fields.Float()
    loan_deduction = fields.Float()
    sal_adv_deduction = fields.Float()
    eos_calc = fields.Float()
    all_leave_balance = fields.Float(store=True, force_save=1)
    leave_balance = fields.Float(compute='_leave_balance', store=True)
    leave_balance_money = fields.Float(compute='_compute_holiday_amount',store=True)
    air_ticket_amount = fields.Float()
    total_amount = fields.Float()
    notes = fields.Text()
    cause_type_amount = fields.Float()
    allowance_total = fields.Float()
    deduction_total = fields.Float()
    loans_total = fields.Float(compute='_compute_loans_totals',store=True)
    net = fields.Float(store=1)
    total_loans = fields.Float(store=1)
    state = fields.Selection(selection=[
        ("draft", "Draft"),
        ("submit", "Submitted"),
        ("direct_manager", "Direct Manager"),
        ("hr_manager", "Department Manager"),
        ("finance_manager", "HR Manager"),
        ("gm_manager", "CEO Manager"),
        ("done", "Complete"),
        ("pay", "Pay"),
        ("cancel", "Refuse")], default='draft', tracking=True)
    from_hr = fields.Boolean()
    # relational fields
    allowance_deduction_ids = fields.One2many('hr.salary.rule.line', 'allowance_deduction_inverse_id')
    cause_type = fields.Many2one('hr.termination.type', tracking=True)
    journal = fields.Many2one('account.journal')
    employee_id = fields.Many2one(comodel_name='hr.employee', string="Employee", default=_get_employee_id,
                                  help='Name of the employee for whom the request is creating',
                                  domain=[('state', '=', 'open')])
    department_id = fields.Many2one(comodel_name='hr.department', string="Department",
                                    related='employee_id.department_id',
                                    help='Department of the employee')
    job_id = fields.Many2one(comodel_name='hr.job', related='employee_id.job_id')
    contract_id = fields.Many2one(comodel_name='hr.contract', related='employee_id.contract_id')
    calculation_method = fields.Many2many('hr.salary.rule')
    loans_ids = fields.Many2many('hr.loan.salary.advance', compute='_get_loans_ids',
                                 domain="[('employee_id', '=', employee_id)]")
    account_move_id = fields.Many2one('account.move')
    salary_termination = fields.Boolean(default=True)

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.onchange('last_work_date')
    def _check_last_date(self):
        for rec in self:
            td = datetime.now().strftime('%Y-%m-%d')
            today = datetime.strptime(td, "%Y-%m-%d").date()
            if str(today) > str(rec.last_work_date):
                raise exceptions.Warning(_('You can Not Request End of Service On a Previous Date'))

    def unlink(self):
        for item in self:
            if item.state != 'draft':
                raise exceptions.Warning(_('You can not delete record in state not in draft'))
        return super(HrTermination, self).unlink()

    # To get salary rules from Termination setting
    @api.onchange('cause_type')
    def _get_salary_rule(self):
        for rec in self:
            rec.calculation_method = False
            if rec.cause_type:
                rec.calculation_method = rec.cause_type.allowance_ids.ids
            else:
                rec.calculation_method = False
        self.re_compute_salary_rules_and_loans()

    @api.onchange('last_work_date')
    def _get_salary_date(self):
        for rec in self:
            if rec.last_work_date:
                date_to = datetime.strptime(str(rec.last_work_date), "%Y-%m-%d").date()
                day = date_to.day
                rec.salary_date_to = date_to
                rec.salary_date_from = date_to - relativedelta.relativedelta(days=day - 1)
            if not rec.first_hire_date:
                raise exceptions.Warning(
                    _('You can not Request End of Service The Employee have Not First Hiring Date'))

    @api.onchange('employee_id', 'last_work_date')
    def _all_holiday_balance(self):
        holiday_balance = self.env['hr.holidays'].search([('type', '=', 'add'),
                                                          ('check_allocation_view', '=', 'balance'),
                                                          ('holiday_status_id.leave_type', '=', 'annual'),
                                                          ('employee_id', '=', self.employee_id.id)],
                                                         limit=1)

        self.all_leave_balance = holiday_balance.remaining_leaves

    # Function to get Yearly holiday balance

    @api.depends('employee_id', 'last_work_date')
    def _leave_balance(self):
        for rec in self:
            leave = self.env['hr.holidays'].search([('type', '=', 'add'),
                                                    ('check_allocation_view', '=', 'balance'),
                                                    ('holiday_status_id.leave_type', '=', 'annual'),
                                                    ('employee_id', '=', rec.employee_id.id)],
                                                   limit=1)
            if leave.holiday_ids and rec.last_work_date and leave.holiday_status_id.duration_ids:
                cron_run_date = datetime.strptime(str(leave.holiday_ids[-1].cron_run_date), "%Y-%m-%d").date()
                date_to_check = (datetime.utcnow() + timedelta(hours=3)).date()
                if cron_run_date < date_to_check:
                    date_to_check = cron_run_date
                to_work_days = (datetime.strptime(str(rec.last_work_date), "%Y-%m-%d").date() -
                                date_to_check).days

                first_hiring_date = datetime.strptime(str(leave.hiring_date), "%Y-%m-%d").date()
                last_work_date = datetime.strptime(str(rec.last_work_date), "%Y-%m-%d").date()
                working_days = (last_work_date - first_hiring_date).days + 1
                working_years = working_days / 365
                for item in leave.holiday_status_id.duration_ids:
                    if item.date_from <= working_years < item.date_to:
                        holiday_duration = item.duration

                upcoming_leave = ((holiday_duration / 12) / 30.39) * to_work_days
                leave_balance = round(rec.employee_id.remaining_leaves + upcoming_leave, 2)

                exceed_days = leave.holiday_status_id.number_of_save_days + holiday_duration
                if leave_balance > exceed_days:
                    rec.leave_balance = exceed_days
                else:
                    rec.leave_balance = round(rec.employee_id.remaining_leaves + upcoming_leave, 2)
                self._compute_holiday_amount()

    def current_date_hijri(self):
        year = datetime.now().year
        day = datetime.now().day
        month = datetime.now().month
        return convert.Gregorian(year, month, day).to_hijri()

    def amount_to_word(self, amount):
        return num2words(amount, lang=self.env.user.lang)

    # Compute holiday amount
    @api.onchange('employee_id', 'leave_balance')
    def _compute_holiday_amount(self):
        for item in self:
            if item.salary:
                day_amount = item.salary / 30
                holiday_amount = item.leave_balance * day_amount
                item.leave_balance_money = holiday_amount

    @api.onchange('salary_termination')
    def _check_last_salary(self):
        if self.salary_termination:
            payslips = self.env['hr.payslip'].search(
                ['&', ('date_from', '>=', self.salary_date_from), ('date_to', '<=', self.salary_date_to),
                 ('employee_id', '=', self.employee_id.id)])
            if payslips:
                raise ValidationError(
                    _('Sorry this payslip is already calculated for this employee %s')
                    % (self.employee_id.name))

    # Compute paid duration
    @api.depends('salary_date_from', 'salary_date_to', 'last_work_date')
    def _get_paid_duration(self):
        for item in self:
            if item.salary_date_from:
                if item.salary_date_to and item.last_work_date:
                    last_work = dt.strptime(str(item.last_work_date), date_format)
                    start_date = dt.strptime(str(item.salary_date_from), date_format)
                    end_date = dt.strptime(str(item.salary_date_to), date_format)
                    if end_date >= start_date:
                        value = relativedelta.relativedelta(end_date, start_date)
                        if value.months < 1:
                            if value.days == 30:
                                item.paid_duration = 31
                            else:
                                item.paid_duration = value.days + 1
                        else:
                            raise exceptions.Warning(_('Duration must be less than or equal month'))
                    else:
                        raise exceptions.Warning(_('Salary Date to must be greater than Salary Date from'))

                    if start_date > last_work:
                        raise exceptions.Warning(_('Salary Date to must be Less than Last Work Date'))

                else:
                    item.paid_duration = 0.0
            else:
                item.paid_duration = 0.0

    # Create rule line in allowance_deduction

    def create_rule_line(self, rule, amount, items, is_advantage, cause_type_factor):
        # If cause type have factor then multiply it in salary rule amount
        if self.cause_type and cause_type_factor == 1:
            if self.cause_type.allowance_id and self.cause_type_amount:
                amount = self.cause_type_amount
        # If cause type have holiday then multiply it in salary rule holiday amount
        holiday_allow = self.cause_type.holiday_allowance
        holiday_deduc = self.cause_type.holiday_deduction
        if holiday_allow and holiday_allow.id == rule.id:
            amount = self.leave_balance_money
        if holiday_deduc and holiday_deduc.id == rule.id:
            amount = -(self.leave_balance_money)
            record = {
                'salary_rule_id': rule.id,
                'amount': amount,
                'is_advantage': is_advantage
            }
            items.append(record)

        if amount > 0 and not holiday_deduc.id == rule.id:
            record = {
                'salary_rule_id': rule.id,
                'amount': amount,
                'is_advantage': is_advantage
            }
            items.append(record)

    def compute_salary_rule(self, rule, items, paid_percentage, advantages, cause_type_factor):
        is_advantage = False
        try:
            if self.employee_id.contract_id:
                if advantages:
                    is_advantage = True
                    if advantages.type == 'customize' and self.contract_id.contractor_type.salary_type == 'amount':
                        amount = advantages.amount / paid_percentage
                    else:
                        amount = advantages.amount
                    if advantages.type == 'exception':
                        amount = (self.compute_rule(rule,
                                                    self.employee_id.contract_id) - advantages.amount) / paid_percentage
                else:
                    amount = self.compute_rule(rule, self.employee_id.contract_id) / paid_percentage
                self.create_rule_line(rule, amount, items, is_advantage, cause_type_factor)

            else:
                raise exceptions.Warning(_('Employee "%s" has no contract') % self.employee_id.name)
        except:
            raise UserError(_('Wrong quantity defined for salary Rule  " %s " ') % (rule.name))
        return amount

    # Compute salary rules

    def compute_rule(self, rule, contract):
        localdict = dict(employee=contract.employee_id, contract=contract)

        if rule.amount_select == 'percentage':
            total_percent = 0
            if rule.related_benefits_discounts:
                for line in rule.related_benefits_discounts:
                    if line.amount_select == 'fix':
                        total_percent += self.compute_rule(line, contract)
                    elif line.amount_select == 'percentage':
                        total_percent += self.compute_rule(line, contract)
                    else:
                        total_percent += self.compute_rule(line, contract)
            if total_percent:
                if rule.salary_type == 'fixed':
                    try:
                        return float(total_percent * rule.amount_percentage / 100)
                    except:
                        raise UserError(
                            _('Wrong percentage base or quantity defined for salary rule %s (%s).') % (
                                rule.name, rule.code))
                elif rule.salary_type == 'related_levels':
                    levels_ids = rule.salary_amount_ids.filtered(
                        lambda item: item.salary_scale_level.id == contract.salary_level.id)
                    if levels_ids:
                        for l in levels_ids:
                            try:
                                return float(l.salary * total_percent / 100)
                            except:
                                raise UserError(
                                    _('Wrong quantity defined for salary rule %s (%s).') % (
                                        rule.name, rule.code))
                    else:
                        return 0
                elif rule.salary_type == 'related_groups':
                    groups_ids = rule.salary_amount_ids.filtered(
                        lambda item: item.salary_scale_group.id == contract.salary_group.id)
                    if groups_ids:
                        for g in groups_ids:
                            try:
                                return float(g.salary * total_percent / 100)
                            except:
                                raise UserError(
                                    _('Wrong quantity defined for salary rule %s (%s).') % (
                                        rule.name, rule.code))
                    else:
                        return 0
                elif rule.salary_type == 'related_degrees':
                    degrees_ids = rule.salary_amount_ids.filtered(
                        lambda item: item.salary_scale_degree.id == contract.salary_degree.id)
                    if degrees_ids:
                        for d in degrees_ids:
                            try:
                                return float(d.salary * total_percent / 100)
                            except:
                                raise UserError(
                                    _('Wrong quantity defined for salary rule %s (%s).') % (
                                        rule.name, rule.code))
                    else:
                        return 0
            else:
                try:
                    return 0
                except:
                    raise Warning(_('There is no total for rule : %s') % (rule.name))

        elif rule.amount_select == 'fix':
            return rule._compute_rule(localdict)[0]

        else:
            return rule._compute_rule(localdict)[0]

    # fill allowance deduction with cause type ,salary_date_from and salary_date_to

    @api.onchange('calculation_method', 'cause_type', 'salary_date_from', 'salary_date_to', 'employee_id')
    def compute_salary_rules_and_loans(self):
        self.re_compute_salary_rules_and_loans()

    # Re-compute salary rules and loans when press re-compute button

    def re_compute_salary_rules_and_loans(self):
        self._get_duration_service()
        self._get_loans_ids()
        self._all_holiday_balance()
        for itemss in self:
            itemss.total_loans = itemss.loans_total
            itemss.net = abs(itemss.allowance_total) - abs(itemss.deduction_total)
            itemss.net -= abs(itemss.total_loans)
        # for item in self:
        # Make the maximum paid duration is 30
        if self.paid_duration > 0:
            if self.paid_duration == 31:
                duration_percentage = 30 / 30
            else:
                duration_percentage = 30 / self.paid_duration
        else:
            duration_percentage = 1

        # Initialize values
        items = []
        self.allowance_deduction_ids = False
        rule_line = self.env['hr.salary.rule.line'].search([('allowance_deduction_inverse_id', '=', False)])
        if rule_line:
            rule_line.unlink()

        # Get all advantages from contract
        if self.contract_id:
            if self.contract_id.advantages:
                for item in self.contract_id.advantages:
                    if item.date_from and item.amount > 0:
                        td = datetime.now().strftime('%Y-%m-%d')
                        today = datetime.strptime(str(td), "%Y-%m-%d").date()
                        start = datetime.strptime(str(item.date_from), "%Y-%m-%d").date()
                        if item.date_to:
                            end = datetime.strptime(str(item.date_to), "%Y-%m-%d").date()

                        # if self.contract_id.contractor_type.salary_type == 'scale' and item.type == 'customize':
                        #    duration_percentage = 1

                        # if exception do not deal with scale or amount
                        if item.date_to:
                            if start <= today < end:
                                amount = self.compute_salary_rule(item.benefits_discounts, items,
                                                                  duration_percentage, item, 0)
                        else:
                            if today >= start:
                                amount = self.compute_salary_rule(item.benefits_discounts, items,
                                                                  duration_percentage, item, 0)

        # Get all salary rules from calculation method
        if self.calculation_method:
            # initialize values
            total, self.salary_for_eos = 0.0, 0.0

            for rule in self.calculation_method:
                total += self.compute_salary_rule(rule, items, duration_percentage, False, 0)
            self.salary_for_eos += total
        else:
            self.salary_for_eos = 0.0

        # Get salary rule  form cause type
        if self.first_hire_date:
            if self.last_work_date:
                if self.cause_type:
                    start_date = dt.strptime(str(self.first_hire_date), "%Y-%m-%d")
                    end_date = dt.strptime(str(self.last_work_date), "%Y-%m-%d")
                    total_rules, amount_of_year, amount_of_month, amount_of_day, self.cause_type_amount = 0.0, 0.0, 0.0, 0.0, 0.0

                    if end_date >= start_date:
                        years = self.service_year
                        days = self.service_day
                        months = self.service_month
                        all_duration = months + (days / 30) + (years * 12)
                        if self.cause_type.allowance_ids and self.cause_type.termination_duration_ids:

                            # Get total for  all salary rules form cause type
                            for rule in self.cause_type.allowance_ids:
                                rule_flag = False
                                # Check if salary rule does  not duplicated when come from contract
                                if items:
                                    for record in items:
                                        if record.get('salary_rule_id') == rule.id and record.get(
                                                'is_advantage') is True:
                                            # Change salary rule value in "salary for eos" by that in contract that is duplicated
                                            total_rules += record.get('amount') * duration_percentage
                                            rule_flag = True

                                if rule_flag is False:
                                    total_rules += self.compute_rule(rule, self.employee_id.contract_id)
                            reward_amount = 0
                            resedual = all_duration
                            line_amount = 0
                            duration_to = 0
                            # search line cause_type and get amount for each line factor
                            for line in self.cause_type.termination_duration_ids:
                                line_amount = line.amount
                                if line.date_to <= all_duration:
                                    if line.amount > 0:
                                        duration_to = line.date_to - duration_to
                                        reward_amount += total_rules * (duration_to / 12) * line.factor
                                        resedual = all_duration - line.date_to

                                else:
                                    if line.date_to > all_duration:
                                        reward_amount += total_rules * resedual / 12 * line.factor
                                        break
                                        resedual = 0

                            reward_amount = reward_amount * line_amount

                            self.cause_type_amount = reward_amount
                            amount = self.compute_salary_rule(self.cause_type.allowance_id, items,
                                                              duration_percentage, False, 1)
                        if self.cause_type.holiday:
                            if self.leave_balance_money >= 0:
                                amount = self.compute_salary_rule(self.cause_type.holiday_allowance, items,
                                                                  duration_percentage, False, 1)
                            if self.leave_balance_money < 0:
                                amount = self.compute_salary_rule(self.cause_type.holiday_deduction, items,
                                                                  duration_percentage, False, 1)

                # update employee last work date
                # self.employee_id.write({'leaving_date': self.last_work_date})

        # Check if salary rule does  not duplicated when come from contract
        if items:
            for record in items:
                for element in items:
                    if record.get('salary_rule_id') == element.get('salary_rule_id'):
                        if record.get('is_advantage') is True and element.get('is_advantage') is False:
                            items.remove(element)

                            # Change salary rule value in "salary for eos" by that in contract that is duplicated
                            rule = self.env['hr.salary.rule'].browse(element.get('salary_rule_id'))
                            self.salary_for_eos -= (self.compute_rule(rule,
                                                                      self.employee_id.contract_id) / duration_percentage)
                            self.salary_for_eos += record.get('amount')

        self.allowance_deduction_ids = [(0, 0, item) for item in items]

        # Compute total allowance ,deduction ,loans and net
        self._leave_balance()
        self._compute_deduction_allowance_total()

    # default loans lines
    @api.depends('employee_id')
    def _get_loans_ids(self):
        record_list = []
        for item in self:
            record_ids = self.env['hr.loan.salary.advance'].search(
                [('state', '=', 'pay'), ('employee_id', '=', item.employee_id.id)])
            if item.employee_id:
                for line in record_ids:
                    if line.employee_id.id == item.employee_id.id:
                        if (line.remaining_loan_amount > 0.0 and line.state == 'pay') or (
                                line.remaining_loan_amount > 0.0 and line.state == 'closed'):
                            record_list.append(line.id)
            item.loans_ids = record_list

    # compute duration service in years , months and days
    @api.onchange('first_hire_date', 'last_work_date', 'employee_id')
    def _get_duration_service(self):
        for item in self:
            if item.first_hire_date and item.last_work_date:
                start_date = dt.strptime(str(item.first_hire_date), "%Y-%m-%d")
                end_date = dt.strptime(str(item.last_work_date), "%Y-%m-%d") + timedelta(days=1)

                if end_date > start_date:
                    unpaid_year = unpaid_month = unpaid_day = 0
                    modules = self.env['ir.module.module'].sudo().search([('state', '=', 'installed'),
                                                                          ('name', '=', 'hr_holidays_public')])
                    if modules:
                        holidays = self.env['hr.holidays'].search(
                            [('holiday_status_id.payslip_type', '=', 'unpaid'),
                             ('holiday_status_id.type_unpaid', '=', 'termaintion'),
                             ('employee_id', '=', self.employee_id.id),
                             ('date_from', '>=', item.first_hire_date),
                             ('date_to', '<=', item.last_work_date),
                             ('state', '=', 'validate1')])
                        for h in holidays:
                            date_from = dt.strptime(str(h.date_from).split()[0], "%Y-%m-%d")
                            date_to = dt.strptime(str(h.date_to).split()[0], "%Y-%m-%d") + timedelta(days=1)
                            r = relativedelta.relativedelta(date_to, date_from)
                            unpaid_year += r.years
                            unpaid_month += r.months
                            unpaid_day += r.days
                            official_holiday_year = h.official_holiday_days and int(h.official_holiday_days / 365) or 0
                            official_holiday_month = h.official_holiday_days and int(
                                (h.official_holiday_days % 365) / 30.5) or 0
                            official_holiday_day = h.official_holiday_days and math.ceil(
                                (h.official_holiday_days % 365) % 30.5) or 0
                            if unpaid_day >= official_holiday_day:
                                unpaid_day = unpaid_day - official_holiday_day
                            else:
                                unpaid_day = 30 - (official_holiday_day - unpaid_day)
                                unpaid_month = unpaid_month - 1
                            if unpaid_month >= official_holiday_month:
                                unpaid_month = unpaid_month - official_holiday_month
                            else:
                                unpaid_month = 12 - (official_holiday_month - unpaid_month)
                                unpaid_year = unpaid_year - 1
                            unpaid_year = unpaid_year - official_holiday_year
                    r = relativedelta.relativedelta(end_date, start_date)
                    year = r.years
                    month = r.months
                    day = r.days
                    item.unpaid_year = unpaid_year
                    item.unpaid_month = unpaid_month
                    item.unpaid_day = unpaid_day
                    if day >= item.unpaid_day:
                        day = day - item.unpaid_day
                    else:
                        day = 30 - (item.unpaid_day - day)
                        month = month - 1
                    if month >= item.unpaid_month:
                        month = month - item.unpaid_month
                    else:
                        month = 12 - (item.unpaid_month - month)
                        year = year - 1
                    year = year - item.unpaid_year

                    item.service_day = day
                    item.service_month = month
                    item.service_year = year
                else:
                    raise exceptions.Warning(
                        _('Leaving Date  must be greater than First Hiring Date'))
            else:
                item.service_year = 0
                item.service_month = 0
                item.service_day = 0
                item.unpaid_year = 0
                item.unpaid_month = 0
                item.unpaid_day = 0

    # compute total loans amount
    @api.depends('loans_ids')
    def _compute_loans_totals(self):
        total = 0.0
        for item in self:
            if item.loans_ids:
                for line in item.loans_ids:
                    total += line.remaining_loan_amount
                item.loans_total = total
        item.total_loans = total

    # compute total allowance and deduction amount
    @api.onchange('allowance_deduction_ids')
    def _compute_deduction_allowance_total(self):
        total_deduction = 0.0
        total_allowance = 0.0
        for item in self.allowance_deduction_ids:
            if item.category_id.rule_type == 'deduction':
                total_deduction += item.amount

            elif item.category_id.rule_type == 'allowance':
                total_allowance += item.amount

            # Other salary rules treat as allowance
            elif item.category_id.rule_type != 'deduction':
                total_allowance += item.amount

        self.deduction_total = total_deduction
        self.allowance_total = total_allowance

    # Compute net
    '''@api.depends('allowance_deduction_ids')
    def _compute_net(self):
        for item in self:
            item.net = abs(item.allowance_total) - abs(item.deduction_total)
            item.net -= abs(item.total_loans)'''

    def set_to_draft(self):
        for item in self:
            state = item.state
            holiday_balance = self.env['hr.holidays'].search([('type', '=', 'add'),
                                                              ('check_allocation_view', '=', 'balance'),
                                                              ('holiday_status_id.leave_type', '=', 'annual'),
                                                              ('employee_id', '=', self.employee_id.id)],
                                                             limit=1)
            last_date = item.write_date.date().month
            # check if the moved journal entry if un posted then delete
            if item.account_move_id:
                if item.account_move_id.state == 'draft':
                    # item.account_move_id.state = 'canceled'
                    item.account_move_id.unlink()
                    item.account_move_id = False
                    self.state = 'draft'
                else:
                    raise exceptions.Warning(_(
                        'You can not re-draft termination because account move with ID "%s" in state Posted') % item.account_move_id.name)

            # Check Employee contract to  Return employee to service
            if state == 'pay':
                if item.employee_id.state == 'out_of_service':
                    if item.employee_id.contract_id.state == 'end_contract':
                        item.employee_id.state = 'open'
                        item.employee_id.leaving_date = False
                        item.employee_id.contract_id.state = 'program_directory'
                        item.employee_id.contract_id.date_end = False

                for loans in item.loans_ids:
                    for install in loans.deduction_lines:
                        if install.paid == True and install.termination_paid == True:
                            install.termination_paid = False
                            install.paid = False
                            loans.state = 'pay'

                holiday_balance.remaining_leaves = item.all_leave_balance
            item.state = 'draft'

    # change status workflow

    def submit(self):
        # Check if exp_custody_petty_cash module is installed
        Module = self.env['ir.module.module'].sudo()
        emp_modules = Module.search([('state', '=', 'installed'), ('name', '=', 'exp_employee_custody')])
        petty_cash_modules = Module.search([('state', '=', 'installed'), ('name', '=', 'hr_expense_petty_cash')])

        # modules = Module.search([('state', '=', 'installed'), ('name', '=', 'exp_custody_petty_cash')])

        if emp_modules:
            # Check if employee has Employee Custody not in state Return done
            employee_custody = self.env['custom.employee.custody'].search(
                [('employee_id', '=', self.employee_id.id), ('state', 'in', ['submit', 'direct', 'admin', 'approve'])])
            if len(employee_custody) > 0:
                raise exceptions.Warning(
                    _(
                        'You can not create termination when there is "%s" employee custody in state not in state Return Done for "%s" please reconcile it') % (
                        len(employee_custody), self.employee_id.name))
        if petty_cash_modules:

            # Check if employee has Employee Petty Cash Payment not in state Return done
            employee_petty_cash_payment =  self.env['petty.cash'].search(
                [('partner_id', '=', self.employee_id.user_id.partner_id.id),
                 ('state', 'in', ['submit', 'direct', 'fm', 'ceo', 'accepted', 'validate'])])
            if len(employee_petty_cash_payment) > 0:
                raise exceptions.Warning(
                    _(
                        'You can not create termination when there is "%s" employee petty cash payment in state not in state Return Done for "%s" please reconcile it') % (
                        len(employee_petty_cash_payment), self.employee_id.name))
        for item in self:
            # Check if Net less than 0.0
            if item.net < 0:
                raise exceptions.Warning(_('Net can not be negative value !!'))
            self.leaves_clearance_constrains()
            item.state = 'submit'

    def direct_manager(self):
        self.leaves_clearance_constrains()
        self.state = 'direct_manager'

    def hr_manager(self):
        self.re_compute_salary_rules_and_loans()
        self.state = 'hr_manager'

    # change status workflow
    def finance_manager(self):
        self.re_compute_salary_rules_and_loans()
        # check for clearance for employee
        employee_clearance = self.env['hr.clearance.form'].search([('employee_id', '=', self.employee_id.id),
                                                                   ('clearance_type', '!=', 'vacation'),
                                                                   ('state', 'in', ['done', 'wait'])])
        if len(employee_clearance) == 0 and self.cause_type.clearance:
            raise exceptions.Warning(
                _('You can not create termination when missing clearance for Employee %s') % self.employee_id.name)
        if self.employee_id:
            #             self.employee_id.state = 'under_out_of_service'
            self.employee_id.contract_id.state = 'end_contract'
        self.state = 'finance_manager'

    def general_manager(self):
        self.state = 'gm_manager'

    def complete(self):
        self.state = 'done'

    def pay(self):
        line_vals = []
        for item in self.allowance_deduction_ids:
            # check if amount greater than 0.0 to fill move account lines
            if item.amount > 0.0:
                # check for deduction credit account
                if item.category_id.rule_type == 'deduction':
                    if not item.account_credit_id:
                        raise exceptions.Warning(
                            _('Undefined credit account for salary rule %s.') % (item.salary_rule_id.name))
                # check for allowance debit account
                elif item.category_id.rule_type == 'allowance':
                    if not item.account_debit_id:
                        raise exceptions.Warning(
                            _('Undefined debit account for salary rule %s.') % (item.salary_rule_id.name))
                else:
                    if not item.account_debit_id:
                        raise exceptions.Warning(_('Check account debit for salary rule "%s" ') % (
                            item.salary_rule_id.name))

                # fill move lines with allowance deduction
                if item.category_id.rule_type == 'allowance':
                    line_vals.append({
                        'name': ('Employee  %s  allowance.') % (self.employee_id.name),
                        'debit': abs(item.amount),
                        'account_id': item.account_debit_id.id,
                        'partner_id': self.employee_id.user_id.partner_id.id})

                elif item.category_id.rule_type == 'deduction':
                    line_vals.append({
                        'name': ('Employee  %s  deduction.') % (self.employee_id.name),
                        'credit': abs(item.amount),
                        'account_id': item.account_credit_id.id,
                        'partner_id': self.employee_id.user_id.partner_id.id})
                else:
                    line_vals.append({
                        'name': ('Employee  %s  rule.') % (self.employee_id.name),
                        'debit': abs(item.amount),
                        'account_id': item.account_debit_id.id,
                        'partner_id': self.employee_id.user_id.partner_id.id})

        for item in self.loans_ids:
            line_vals.append({
                'name': ('Employee  %s  loans.') % (self.employee_id.name),
                'credit': abs(item.remaining_loan_amount),
                'account_id': item.request_type.account_id.id,
                'partner_id': self.employee_id.user_id.partner_id.id})

        line_vals.append({
            'name': ('Employee  %s  Net.') % (self.employee_id.name),
            'credit': abs(self.net),
            'account_id': self.journal.default_account_id.id,
            'partner_id': self.employee_id.user_id.partner_id.id})

        move = self.env['account.move'].create({
            'state': 'draft',
            'journal_id': self.journal.id,
            'date': date.today(),
            'ref': 'Termination of "%s" ' % self.employee_id.name,
            'line_ids': [(0, 0, value) for value in line_vals]
        })

        for item in self.loans_ids:
            # last_date = datetime.strptime(str(self.write_date), "%Y-%m-%d %H:%M:%S").date().month
            for install in item.deduction_lines:
                # loan_date = datetime.strptime(str(install.write_date), "%Y-%m-%d %H:%M:%S").date().month
                # if loan_date >= last_date and not install.paid:
                if not install.paid:
                    install.paid = True
                    install.termination_paid = True
                    item.state = 'closed'
        self.write({'account_move_id': move.id})

        # update employee last work date
        if self.last_work_date:
            self.employee_id.write({'leaving_date': self.last_work_date})
            self.employee_id.contract_id.write({'date_end': self.last_work_date})
        for item in self:
            # Change employee state when termination to "Out Of Service"
            # Change employee contract state to "End Contract"
            if item.employee_id:
                item.employee_id.contract_id.state = 'end_contract'
                item.employee_id.state = 'out_of_service'
        holiday_balance = self.env['hr.holidays'].search([('type', '=', 'add'),
                                                                  ('check_allocation_view', '=', 'balance'),
                                                                  ('holiday_status_id.leave_type', '=', 'annual'),
                                                                  ('employee_id', '=', self.employee_id.id)],
                                                                 limit=1)
        holiday_balance.remaining_leaves = 0
        self.state = 'pay'



    def cancel(self):
        self.state = 'cancel'

    # check for employee unclosed leaves and check for clearance for employee constrain

    @api.constrains('employee_id')
    def leaves_clearance_constrains(self):

        # check for employee unclosed leaves
        employee_holidays = self.env['hr.holidays'].search(
            [('employee_id', '=', self.employee_id.id), ('type', '=', 'remove'),
             ('state', 'not in', ['refuse', 'validate1', 'cancel'])], limit=1)
        if len(employee_holidays) > 0:
            raise exceptions.Warning(
                _('Sorry ! This Employee have un approved or Reject Holiday Request : \n %s') % (
                    employee_holidays.holiday_status_id.name))

        # check for clearance for employee
        '''employee_clearance = self.env['hr.clearance.form'].search(
            [('employee_id', '=', self.employee_id.id), ('state', 'not in', ['draft', 'refuse'])])
        if len(employee_clearance) == 0 and self.cause_type.clearance == True:
            raise exceptions.Warning(
                _('You can not create termination when missing clearance for "%s"') % self.employee_id.name)'''

    # Override create function

    @api.constrains('employee_id')
    def net_constains(self):
        if self.net < 0.0:
            raise exceptions.Warning(_('The Net must be not negative value .'))


class HrTerminationType(models.Model):
    _name = 'hr.termination.type'

    name = fields.Char(translate=True)
    year = fields.Integer()
    clearance = fields.Boolean()
    factor = fields.Float()
    holiday = fields.Boolean()
    holiday_allowance = fields.Many2one('hr.salary.rule', domain=[('rules_type', '=', 'termination'),
                                                                  ('category_id.rule_type', '=', 'allowance')])
    holiday_deduction = fields.Many2one('hr.salary.rule', domain=[('rules_type', '=', 'termination'),
                                                                  ('category_id.rule_type', '=', 'deduction')])

    # Relational fields
    allowance_ids = fields.Many2many('hr.salary.rule')
    allowance_id = fields.Many2one('hr.salary.rule', domain=[('rules_type', '=', 'termination'),
                                                             ('category_id.rule_type', '=', 'allowance')])
    termination_duration_ids = fields.Many2many('hr.termination.duration')

    def unlink(self):
        for item in self:
            i = self.env['hr.termination'].search([('cause_type', '=', item.id)])
            if i:
                raise exceptions.Warning(
                    _('You can not delete record There is a related other record %s termination') % i.employee_id.id.name)
        return super(HrTerminationType, self).unlink()

    @api.constrains('holiday_allowance', 'allowance_id')
    def _check_allowance_id(self):
        for allowance in self:
            if allowance.allowance_id.id == allowance.holiday_allowance.id:
                raise ValidationError(
                    _('You cannot chosen The same allowance at the end of service and holiday allowance'))


class HrTerminationDuration(models.Model):
    _name = 'hr.termination.duration'

    name = fields.Char(translate=True, required=True)
    date_from = fields.Float()
    date_to = fields.Float()
    factor = fields.Float()
    amount = fields.Float()


class HrAllowanceDeduction(models.Model):
    _name = 'hr.allowance.deduction'

    name = fields.Char()
    amount = fields.Float()

    # relational fields
    type = fields.Many2one('hr.salary.rule')
    account_credit_id = fields.Many2one('account.account', related='type.rule_credit_account_id')
    account_debit_id = fields.Many2one('account.account', related='type.rule_debit_account_id')


class HrSalaryRuleAndLoansLines(models.Model):
    _name = 'hr.salary.rule.line'

    amount = fields.Float()
    is_advantage = fields.Boolean()

    # Relational fields
    allowance_deduction_inverse_id = fields.Many2one('hr.termination')  # Inverse
    salary_rule_id = fields.Many2one('hr.salary.rule')
    category_id = fields.Many2one('hr.salary.rule.category', related='salary_rule_id.category_id', readonly=True,
                                  required=False)
    account_credit_id = fields.Many2one('account.account', related='salary_rule_id.rule_credit_account_id',
                                        readonly=True, required=False)
    account_debit_id = fields.Many2one('account.account', related='salary_rule_id.rule_debit_account_id', readonly=True,
                                       required=False)
