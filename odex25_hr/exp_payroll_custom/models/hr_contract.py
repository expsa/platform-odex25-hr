# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HrContractSalaryScale(models.Model):
    _inherit = 'hr.contract'

    salary_level = fields.Many2one(comodel_name='hr.payroll.structure', domain=[('id', 'in', [])])
    salary_scale = fields.Many2one(comodel_name='hr.payroll.structure', domain=[('id', 'in', [])], index=True)
    salary_group = fields.Many2one(comodel_name='hr.payroll.structure', domain=[('id', 'in', [])])
    salary_degree = fields.Many2one(comodel_name='hr.payroll.structure', domain=[('id', 'in', [])])
    hide = fields.Boolean(string='Hide', compute="compute_type")
    required_condition = fields.Boolean(string='Required Condition', compute='compute_move_type')
    total_allowance = fields.Float(string='Total Allowance', compute='compute_function')
    total_deduction = fields.Float(string='Total Deduction', compute='compute_function')
    total_net = fields.Float(string='Total Net', compute='compute_function')
    advantages = fields.One2many('contract.advantage', 'contract_advantage_id', string='Advantages')
    house_allowance_temp = fields.Float(string='House Allowance', compute='compute_function')
    transport_allowance = fields.Float(string='Transport Allowance', compute='compute_function')
    transport_allowance_temp = fields.Float(string='Transportation Allowance', compute='_get_amount')
    field_allowance_temp = fields.Float(string='Field Allowance', compute='_get_amount')
    special_allowance_temp = fields.Float(_('Special Allowance'), compute='_get_amount')
    other_allowance_temp = fields.Float(_('Other Allowances'), compute='_get_amount')
    travel_allowance_temp = fields.Float(_('Travel Allowance'), compute='_get_amount')
    education_allowance_temp = fields.Float(_('Education Allowance'), compute='_get_amount')
    food_allowance2_temp = fields.Float(_('Food Allowance'), compute='_get_amount')
    security_allowance_temp = fields.Float(_('Security Allowance'), compute='_get_amount')
    transport_allowance_type = fields.Selection(
        [('none', _('None')), ('perc', _('Percentage')), ('num', _('Number')), ('company', 'By Company')],
        _('Transportation Allowance Type'), default='none')
    field_allowance_type = fields.Selection(
        [('none', _('None')), ('perc', _('Percentage')), ('num', _('Number')), ('company', 'By Company')],
        _('Field Allowance Type'), default='none')
    field_allowance = fields.Float(_('Field Allowance'))


    special_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                              _('Special Allowance Type'), default='none')
    special_allowance = fields.Float(_('Special Allowance'))

    other_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                            _('Other Allowances Type'), default='none')
    other_allowance = fields.Float(_('Other Allowances'))

    travel_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                             _('Travel Allowance Type'), default='none')
    travel_allowance = fields.Float(_('Travel Allowance'))

    education_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                                _('Education Allowance Type'), default='none')
    education_allowance = fields.Float(_('Education Allowance'))

    food_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                           _('Food Allowance Type'), default='none')
    food_allowance2 = fields.Float(_('Food Allowance'))

    security_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                               _('Security Allowance Type'), default='none')
    security_allowance = fields.Float(_('Security Allowance'))

    house_allowance_type = fields.Selection([('none', 'None'), ('perc', 'Percentage'), ('num', 'Number')],
                                            'House Allowance Type', default='none')
    house_allowance = fields.Float('House Allowance')

    communication_allowance_type = fields.Selection(
        [('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
        _('Communication Allowance Type'), default='none')
    communication_allowance = fields.Float(_('Communication Allowance'))
    communication_allowance_temp = fields.Float(_('Communication Allowance'), compute='_get_amount')

    retire_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                             _('Retire Allowance Type'), default='none')
    retire_allowance = fields.Float(_('Retirement Allowance'))

    infect_allowance_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                             _('Infection Allowance Type'), default='none')
    infect_allowance = fields.Float(_('Infection Allowance'))
    supervision_allowance_type = fields.Selection(
        [('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
        _('Supervision Allowance Type'), default='none')
    supervision_allowance = fields.Float(_('Supervision Allowance'))

    other_deduction_type = fields.Selection([('none', _('None')), ('perc', _('Percentage')), ('num', _('Number'))],
                                            _('Other Deductions Type'), default='none')
    other_deduction = fields.Float(_('Other Deductions'))
    gosi_deduction = fields.Float(compute="_calculate_gosi", string='Gosi (Employee Percentage)')
    gosi_employer_deduction = fields.Float(compute="_calculate_gosi", string='Gosi (Employer Percentage)')
    total_gosi = fields.Float(compute="_calculate_gosi", string='Total')


    @api.constrains('advantages', 'salary', 'salary_group')
    def amount_constrains(self):
        localdict = dict(employee=self.employee_id.id, contract=self.env['hr.contract'].search([
            ('employee_id', '=', self.employee_id.id)]))
        if self.salary_group.gread_max > 0 and self.salary_group.gread_min > 0:
            if self.salary > self.salary_group.gread_max or self.salary < self.salary_group.gread_min:
                raise UserError(_('The Basic Salary Is Greater Than Group Gread Max Or less than Gread Min'))
        for item in self.advantages:
            item.to_get_contract_id()
            if item.benefits_discounts._compute_rule(localdict)[0] < item.amount and item.type == 'exception':
                raise UserError(_(
                    'The amount you put is greater than fact value of this Salary rule %s (%s).') % (
                                    item.benefits_discounts.name, item.benefits_discounts.code))

    @api.depends('salary_scale.transfer_type')
    def compute_move_type(self):
        if self.salary_scale.transfer_type == 'one_by_one':
            self.required_condition = True
        else:
            self.required_condition = False

    @api.depends()
    def _calculate_gosi(self):
        saudi_gosi = self.env.user.company_id.saudi_gosi
        company_gosi = self.env.user.company_id.company_gosi
        none_saudi_gosi = self.env.user.company_id.none_saudi_gosi
        for record in self:
            if (record.emp_type == 'saudi' or record.emp_type == 'displaced') and record.is_gosi_deducted == "yes":
                employee_gosi = (record.salary_insurnce + record.house_allowance_temp) * saudi_gosi / 100
                employer_gosi = (record.salary_insurnce + record.house_allowance_temp) * company_gosi / 100
                record.gosi_deduction = employee_gosi
                record.gosi_employer_deduction = employer_gosi
                record.total_gosi = employee_gosi + employer_gosi

            elif (record.emp_type == 'saudi' or record.emp_type == 'displaced') and record.is_gosi_deducted == "no":

                employee_gosi = (record.salary_insurnce + record.house_allowance_temp) * saudi_gosi / 100
                employer_gosi = (record.salary_insurnce + record.house_allowance_temp) * company_gosi / 100

                record.gosi_deduction = 0.0
                record.gosi_employer_deduction = employee_gosi + employer_gosi
                record.total_gosi = employee_gosi + employer_gosi
            else:
                # pass
                employer_gosi = (record.salary_insurnce + record.house_allowance_temp) * none_saudi_gosi / 100

                record.gosi_deduction = 0.0
                record.gosi_employer_deduction = employer_gosi
                record.total_gosi = employer_gosi

            if (record.emp_type == 'saudi' or record.emp_type == 'displaced') and record.saudi_emp_type == 'saudi-non':
                record.gosi_deduction = 0.0
                record.gosi_employer_deduction = 0.0
                record.total_gosi = 0.0

    @api.depends('salary_scale', 'salary_level', 'salary_group', 'salary_degree')
    def compute_function(self):
        for item in self:
            item.house_allowance_temp = 0
            item.transport_allowance = 0
            item.total_net = 0
            contract = self.env['hr.contract'].search([('employee_id', '=', item.employee_id.id)])
            localdict = dict(employee=item.employee_id.id, contract=contract)
            current_date = datetime.now().date()

            # customize type in advantages
            allowance_customize_items = item.advantages.filtered(
                lambda key: key.type == 'customize' and key.out_rule is False and
                key.benefits_discounts.category_id.rule_type == 'allowance' and
                (datetime.strptime(str(key.date_to), "%Y-%m-%d").date() if key.date_to else current_date)
                >= current_date >= datetime.strptime(str(key.date_from), "%Y-%m-%d").date())

            allow_sum_custom = sum(x.amount for x in allowance_customize_items)
            for x in allowance_customize_items:
                if x.benefits_discounts.rules_type == 'house':
                    item.house_allowance_temp += x.amount
            # allow_custom_ids = [record.benefits_discounts.id for record in allowance_customize_items]

            deduction_customize_items = item.advantages.filtered(
                lambda key: key.type == 'customize' and key.out_rule is False and
                            key.benefits_discounts.category_id.rule_type == 'deduction' and
                            (datetime.strptime(str(key.date_to), "%Y-%m-%d").date() if key.date_to else current_date)
                            >= current_date >= datetime.strptime(str(key.date_from), "%Y-%m-%d").date())

            ded_sum_custom = sum(x.amount for x in deduction_customize_items)
            ded_custom_ids = [record.benefits_discounts.id for record in deduction_customize_items]

            # exception type in advantages
            exception_items = item.advantages.filtered(lambda key: key.type == 'exception')
            total_rule_result, sum_except, sum_customize_expect = 0.0, 0.0, 0.0

            for x in exception_items:
                rule_result = x.benefits_discounts._compute_rule(localdict)[0]
                if x.date_from >= str(current_date):
                    total_rule_result = rule_result
                elif str(current_date) > x.date_from:
                    if x.date_to and str(current_date) <= x.date_to:
                        total_rule_result = rule_result - x.amount
                    elif x.date_to and str(current_date) >= x.date_to:
                        total_rule_result = 0  # rule_result
                    elif not x.date_to:
                        total_rule_result = rule_result - x.amount
                else:
                    if rule_result > x.amount:
                        total_rule_result = rule_result - x.amount

                if total_rule_result:
                    if x.benefits_discounts.category_id.rule_type == 'allowance':
                        sum_customize_expect += total_rule_result
                        if x.benefits_discounts.rules_type == 'house':
                            item.house_allowance_temp += total_rule_result - x.amount
                    else:
                        sum_except += total_rule_result

            if exception_items:
                exception_items = item.advantages.filtered(
                    lambda key: (datetime.strptime(str(key.date_to),
                                                   "%Y-%m-%d").date().month if key.date_to else current_date.month)
                                >= current_date.month >= datetime.strptime(str(key.date_from), "%Y-%m-%d").date().month)

            except_ids = [record.benefits_discounts.id for record in exception_items]

            rule_ids = item.salary_scale.rule_ids.filtered(
                lambda key: key.id not in ded_custom_ids and key.id not in except_ids)

            level_rule_ids = item.salary_level.benefits_discounts_ids.filtered(lambda key: key.id not in except_ids)
            # key.id not in allow_custom_ids and key.id not in ded_custom_ids and

            group_rule_ids = item.salary_group.benefits_discounts_ids.filtered(lambda key: key.id not in except_ids)
            # key.id not in allow_custom_ids and key.id not in ded_custom_ids and

            total_allowance = 0
            total_ded = 0
            for line in rule_ids:
                if line.category_id.rule_type == 'allowance':
                    total_allowance += line._compute_rule(localdict)[0]

                if line.category_id.rule_type == 'deduction':
                    total_ded += line._compute_rule(localdict)[0]

                if line.rules_type == 'house':
                    item.house_allowance_temp += line._compute_rule(localdict)[0]
                if line.rules_type == 'transport':
                    item.transport_allowance += line._compute_rule(localdict)[0]

                item.total_allowance = total_allowance
                item.total_deduction = -total_ded

            if item.salary_level:
                total_allowance = 0
                total_deduction = 0
                for line in level_rule_ids:
                    if line.category_id.rule_type == 'allowance':
                        total_allowance += line._compute_rule(localdict)[0]
                    elif line.category_id.rule_type == 'deduction':
                        total_deduction += line._compute_rule(localdict)[0]

                item.total_allowance += total_allowance
                item.total_deduction += -total_deduction

            if item.salary_group:
                total_allowance = 0
                total_deduction = 0
                for line in group_rule_ids:
                    if line.category_id.rule_type == 'allowance':
                        total_allowance += line._compute_rule(localdict)[0]
                    elif line.category_id.rule_type == 'deduction':
                        total_deduction += line._compute_rule(localdict)[0]

                item.total_allowance += total_allowance
                item.total_deduction += -total_deduction

            item.total_allowance += allow_sum_custom
            item.total_allowance += sum_customize_expect
            item.total_deduction += -ded_sum_custom
            item.total_deduction += -sum_except
            item.total_net = item.total_allowance + item.total_deduction

    # filter salary_level,salary_group,salary_degree

    @api.onchange('salary_scale')
    def onchange_salary_scale(self):
        for item in self:
            if item.salary_scale:
                level_ids = self.env['hr.payroll.structure'].search(
                    [('salary_scale_id', '=', item.salary_scale.id), ('type', '=', 'level')])
                group_ids = self.env['hr.payroll.structure'].search(
                    [('salary_scale_id', '=', item.salary_scale.id), ('type', '=', 'group')])
                degree_ids = self.env['hr.payroll.structure'].search(
                    [('salary_scale_id', '=', item.salary_scale.id), ('type', '=', 'degree')])
                return {'domain': {'salary_level': [('id', 'in', level_ids.ids)],
                                   'salary_group': [('id', 'in', group_ids.ids)],
                                   'salary_degree': [('id', 'in', degree_ids.ids)]}}
            else:
                item.total_allowance = 0.0
                item.total_deduction = 0.0
                item.total_net = 0.0
                return {'domain': {'salary_level': [('id', 'in', [])],
                                   'salary_group': [('id', 'in', [])],
                                   'salary_degree': [('id', 'in', [])]}}

    # filter depend on salary_level

    @api.onchange('salary_level')
    def onchange_salary_level(self):
        for item in self:
            if item.salary_level:
                group_ids = self.env['hr.payroll.structure'].search(
                    [('salary_scale_level_id', '=', item.salary_level.id), ('type', '=', 'group')])
                return {'domain': {'salary_group': [('id', 'in', group_ids.ids)],
                                   'salary_degree': [('id', 'in', [])]}}
            else:
                return {'domain': {'salary_group': [('id', 'in', [])],
                                   'salary_degree': [('id', 'in', [])]}}

    # filter depend on salary_group

    @api.onchange('salary_group')
    def onchange_salary_group(self):
        for item in self:
            if item.salary_group:
                degree_ids = self.env['hr.payroll.structure'].search(
                    [('salary_scale_group_id', '=', item.salary_group.id), ('type', '=', 'degree')])
                return {'domain': {'salary_degree': [('id', 'in', degree_ids.ids)]}}
            else:
                return {'domain': {'salary_degree': [('id', 'in', [])]}}

    @api.depends('salary_degree')
    def _get_amount(self):
        for record in self:
            record.transport_allowance_temp = record.transport_allowance * record.wage / 100 \
                if record.transport_allowance_type == 'perc' else record.transport_allowance
            record.house_allowance_temp = record.house_allowance * record.wage / 100 \
                if record.house_allowance_type == 'perc' else record.house_allowance
            record.communication_allowance_temp = record.communication_allowance * record.wage / 100 \
                if record.communication_allowance_type == 'perc' else record.communication_allowance
            record.field_allowance_temp = record.field_allowance * record.wage / 100 \
                if record.field_allowance_type == 'perc' else record.field_allowance
            record.special_allowance_temp = record.special_allowance * record.wage / 100 \
                if record.special_allowance_type == 'perc' else record.special_allowance
            record.other_allowance_temp = record.other_allowance * record.wage / 100 \
                if record.other_allowance_type == 'perc' else record.other_allowance

    @api.depends('contractor_type.salary_type')
    def compute_type(self):
        if self.contractor_type.salary_type == 'scale':
            self.hide = True
        else:
            self.hide = False


class Advantages(models.Model):
    _name = 'contract.advantage'
    _rec_name = 'benefits_discounts'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    amount = fields.Float(string='Amount', tracking=True)
    type = fields.Selection(selection=[('customize', _('Customize')),
                                       ('exception', _('Exception'))], string='Type', default="customize")
    # to link employee move line from official mission to advantages line in contract
    official_mission_id = fields.Boolean(string="Official Mission", default=False)
    # To link employee move line from over time to advantages line in contract
    over_time_id = fields.Boolean(string="OverTime", default=False)
    # To link employee move line from employee reward to advantages line in contract
    reward_id = fields.Boolean(string="Reward", default=False)
    penalty_id = fields.Boolean(string='Penalty Name', default=False)

    # Relational fields
    benefits_discounts = fields.Many2one(comodel_name='hr.salary.rule', string='Benefits/Discounts')
    contract_advantage_id = fields.Many2one('hr.contract')
    done = fields.Boolean(string="Done in Payroll")
    out_rule = fields.Boolean(string="Out of Payroll", default=True)

    employee_id = fields.Many2one('hr.employee', 'Employee Name', domain=[('state', '=', 'open')], tracking=True)
    state = fields.Selection(selection=[('draft', _('Draft')), ('confirm', _('Confirmed')),
                                        ('refused', _('Refused'))],
                             default='draft', tracking=True)

    comments = fields.Text(string='Comments')
    payroll_month = fields.Text(string='Payroll Month', tracking=True)

    @api.constrains('date_from', 'date_to', 'amount')
    def _chick_date(self):
        for rec in self:
            if rec.date_to:
                if rec.date_to <= rec.date_from:
                    raise UserError(_('The Date Form Must be Less than Date To'))
            if rec.amount <= 0:
              raise UserError(_('The Amount Must be Greater Than Zero The Employee %s')% rec.employee_id.name)

    def confirm(self):
        self.state = 'confirm'

    def refused(self):
        self.state = 'refused'

    def draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.onchange('employee_id')
    def to_get_contract_id(self):
        contract_id = self.employee_id.contract_id
        self.employee_id = self.contract_advantage_id.employee_id.id
        if contract_id:
            self.contract_advantage_id = contract_id.id
            self.employee_id = self.contract_advantage_id.employee_id.id
        else:
            return False

    def unlink(self):
        for item in self:
            if item.state != 'draft':
                raise UserError(_('You cannot delete The Salary rule %s For the Employee %s is Not Draft') % (
                    item.benefits_discounts.name, item.employee_id.name))
            # if item.done == True:
            #     raise UserError(_('Sorry, The Salary rule %s For the Employee %s is Already Computed in Payroll') % (
            #     item.benefits_discounts.name, item.employee_id.name))
        return super(Advantages, self).unlink()

    @api.constrains('employee_id', 'date_from', 'date_to', 'benefits_discounts')
    def check_rule_dates(self):
        """ Function Can Not add Same Advantage at The Same Month
            same employee.
        """
        for rec in self:
            domain = [
                ('date_from', '<=', rec.date_to),
                ('date_to', '>=', rec.date_from),
                ('employee_id', '=', rec.employee_id.id),
                ('id', '!=', rec.id),
                ('benefits_discounts', '=', rec.benefits_discounts.id), ]
            advantages_id = self.search_count(domain)
            if advantages_id:
                # for adv in advantages_id:
                raise UserError(
                    _('You Can Not add Same Allowance/Deduction at The Same Employee %s For The Same Month!')
                    % rec.employee_id.name)
