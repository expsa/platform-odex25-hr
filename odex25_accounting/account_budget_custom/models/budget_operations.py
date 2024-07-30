# -*- coding: utf-8 -*-
##############################################################################
#
#    Expert Co. Ltd.
#    Copyright (C) 2018 (<http://www.exp-sa.com/>).
#
##############################################################################

from odoo import api, fields, models, _
from odoo.tools import ustr
from odoo.exceptions import UserError, ValidationError


class BudgetOperations(models.Model):
    """
    this model used to make operations on budget
    """
    _name = 'budget.operations'
    _description = 'Budget Operations'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Name', default='/'
    )
    department_id = fields.Many2one(
        comodel_name='hr.department',
        string='Department',
    )
    from_crossovered_budget_id = fields.Many2one(
        comodel_name='crossovered.budget',
        string='Budget', tracking=True
    )
    from_budget_line_id = fields.Many2one(
        comodel_name='crossovered.budget.lines',
        string='Cost Center', tracking=True
    )
    to_crossovered_budget_id = fields.Many2one(
        comodel_name='crossovered.budget',
        string='Budget', tracking=True
    )
    to_budget_line_id = fields.Many2one(
        comodel_name='crossovered.budget.lines',
        string='Cost Center', tracking=True
    )
    amount = fields.Monetary(
        string='Amount',
        required=True, tracking=True
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency', readonly=True, required=True,
        default=lambda self: self.env.user.company_id.currency_id.id
    )
    state = fields.Selection(
        selection=[('draft', 'Draft'),
                   ('confirmed', 'Confirmed')],
        default='draft', string='Status', readonly=True, tracking=True
    )
    type = fields.Selection(
        selection=[('unlock', 'Unlock'),
                   ('transfer', 'Transfer')],
        default='transfer', string='type', readonly=True, tracking=True
    )
    date = fields.Date()
    from_reserved = fields.Boolean(string='Reserve?', tracking=True)
    from_budget_post_id = fields.Many2one(
        comodel_name='account.budget.post',
        string='Budget Post', tracking=True
    )
    to_budget_post_id = fields.Many2one(
        comodel_name='account.budget.post',
        string='Budget Post', tracking=True
    )
    operation_type = fields.Selection(
        selection=[('transfer', 'Transfer'),
                   ('increase', 'Increase'),
                   ('decrease', 'Decrease')],
        default='transfer', string='Operation Type', required=True, tracking=True
    )

    @api.onchange('from_crossovered_budget_id', 'operation_type')
    def get_budget_domain_year(self):
        for rec in self:
            domain = [('id','=',False)]
            if rec.operation_type == 'transfer' and rec.from_crossovered_budget_id:
                date_to = rec.from_crossovered_budget_id.date_to
                record = rec.env['crossovered.budget'].sudo().search([('date_to', '>', str(date_to))])
                if record:
                    domain = [('id', 'in', record.mapped('crossovered_budget_line.general_budget_id').ids)]
            else:
                domain = [('id', 'in', rec.env['account.budget.post'].sudo().search([]).ids)]
            return {
                'domain': {
                    'to_budget_post_id': domain,
                }
            }

    @api.model
    def create(self, values):
        sequence_code = 'budget_operation.seq'
        values['name'] = self.env['ir.sequence'].with_context(
            ir_sequence_date=values['date']).next_by_code(sequence_code)
        return super(BudgetOperations, self).create(values)

    @api.onchange('operation_type')
    def _onchange_operation_type(self):
        if self.operation_type == 'increase':
            self.from_crossovered_budget_id = False
            self.from_budget_line_id = False
            self.from_budget_post_id = False
            self.from_reserved = False

    @api.onchange('from_budget_post_id')
    def _onchange_from_budget_post(self):
        domain = [('id', 'in', [])]
        if self.from_budget_post_id:
            budget_line_obj = self.env['crossovered.budget.lines']
            budget_line = budget_line_obj.read_group([('general_budget_id', '=', self.from_budget_post_id.id)],
                                                     ['crossovered_budget_id'], ['crossovered_budget_id'])
            domain = [('id', 'in', [bl['crossovered_budget_id'][0] for bl in budget_line])]
        self.from_crossovered_budget_id = False
        self.from_budget_line_id = False
        return {
            'domain': {
                'from_crossovered_budget_id': domain,
            }
        }

    @api.onchange('to_budget_post_id')
    def _onchange_to_budget_post(self):
        domain = [('id', 'in', [])]
        if self.to_budget_post_id:
            budget_line_obj = self.env['crossovered.budget.lines']
            search_domain = [('general_budget_id', '=', self.to_budget_post_id.id)]
            if self.operation_type == 'transfer':
                search_domain+=[ ('date_to', '>', str(self.from_crossovered_budget_id.date_to))]
            budget_line = budget_line_obj.search(search_domain)
            domain = [('id', 'in', budget_line.mapped('crossovered_budget_id').ids)]
        self.to_crossovered_budget_id = False
        self.to_budget_line_id = False
        return {
            'domain': {
                'to_crossovered_budget_id': domain,
            }
        }

    @api.onchange('from_crossovered_budget_id')
    def _onchange_from_crossovered_budget(self):
        return {
            'domain': {
                'from_budget_line_id':
                    [('crossovered_budget_id', '=', self.from_crossovered_budget_id.id),
                     ('general_budget_id', 'in', [self.from_budget_post_id.id])]
            }
        }

    @api.onchange('to_crossovered_budget_id')
    def _onchange_to_crossovered_budget(self):
        return {
            'domain': {
                'to_budget_line_id':
                    [('crossovered_budget_id', '=', self.to_crossovered_budget_id.id),
                     ('general_budget_id', 'in', [self.to_budget_post_id.id])]
            }
        }

    def to_draft(self):
        """
        set the current operation on budgets to draft
        """
        self.state = 'draft'

    def confirm(self):
        """
        confirm the current operation on budgets
        """
        transfer = True if self.operation_type =='transfer' else False
        self.from_budget_line_id._check_amount(self.amount,transfer)
        if self.type == 'unlock':
            self.from_reserved = True
            self.to_crossovered_budget_id = self.from_crossovered_budget_id.id
            self.to_budget_line_id = self.from_budget_line_id.id
        self.state = 'confirmed'
