# -*- coding: utf-8 -*-
##############################################################################
#
#   Expert (LCT, Life Connection Technology)
#    Copyright (C) 2021-2022 LCT
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Project(models.Model):
    _inherit = 'project.project'
    _description = "Project Kh Custom"

    eng_installment_line_ids = fields.One2many('line.contract.installment', 'project_id',
                                               domain=[('payment_type', '=', 'engineering')], string="Engineering Payment")
    con_installment_line_ids = fields.One2many('line.contract.installment', 'project_id',
                                               domain=[('payment_type', '=', 'contractor')], string="Contractor Payment")
    eng_contract_ids = fields.One2many('contract.contract', 'project_id',
                                               domain=[('con_type', '=', 'engineering')], string="Engineering Contract")
    cont_contract_ids = fields.One2many('contract.contract', 'project_id',
                                               domain=[('con_type', '=', 'contractor')], string="Contractor Contract")
    eng_contract_counts = fields.Integer(string='Engineering', compute='count_contract_number')
    con_contract_counts = fields.Integer(string='Contractor', compute='count_contract_number')

    def count_contract_number(self):
        con_contract_counts = self.env['contract.contract'].search_count([('project_id', '=', self.id),
                                                                           ('con_type', '=', 'contractor')])
        eng_contract_counts = self.env['contract.contract'].search_count([('project_id', '=', self.id),
                                                                           ('con_type', '=', 'engineering')])

        self.con_contract_counts = con_contract_counts
        self.eng_contract_counts = eng_contract_counts


    def get_payment_amount(self):
        suppl_payment_amount = sum(self.project_expense_ids.mapped('amount'))
        engineering_payment_ids = self.env['line.contract.installment'].search([('project_id', '=', self.id),
                                                                                  ('payment_type', '=', 'engineering')])
        subcontractor_payment_ids = self.env['line.contract.installment'].search([('project_id', '=', self.id),
                                                                          ('payment_type', '=', 'contractor')])

        self.suppl_payment_amount = suppl_payment_amount
        self.engineer_payment_amount = sum(engineering_payment_ids.mapped('amount'))
        self.subcontractor_payment_amount = sum(subcontractor_payment_ids.mapped('amount'))
        self.total_payment = suppl_payment_amount + sum(engineering_payment_ids.mapped('amount')) + sum(subcontractor_payment_ids.mapped('amount'))


    def get_contractor_contract(self):
        contractor_contract_ids = self.env['contract.contract'].search([('project_id', '=', self.id),
                                                                                  ('con_type', '=', 'contractor')])
        form_id = self.env.ref('khawald_project_contract.contract_contract_form_view_contractor').id
        tree_id = self.env.ref('contract.contract_contract_tree_view').id
        domain = [('id', 'in', contractor_contract_ids.ids)]
        return {
            'name': _('Contractor Contract'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'contract.contract',
            'views': [(tree_id, 'tree'), (form_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {'search_default_project_id': self.id,
                        'default_project_id': self.id,
                        'default_con_type': 'engineering',
                        'is_contract': 1,
                        'search_default_not_finished': 1,
                        'search_default_con_type': 'contractor',
                        'default_contract_type': 'sale'},
            'domain': domain,
        }

    def get_engineering_contract(self):
        contractor_contract_ids = self.env['contract.contract'].search([('project_id', '=', self.id),
                                                                        ('con_type', '=', 'engineering')])
        form_id = self.env.ref('khawald_project_contract.contract_contract_form_view_engineering').id
        tree_id = self.env.ref('contract.contract_contract_tree_view').id
        domain = [('id', 'in', contractor_contract_ids.ids)]
        return {
            'name': _('Engineering Contract'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'contract.contract',
            'views': [(tree_id, 'tree'), (form_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {'search_default_project_id': self.id,
                        'default_project_id': self.id,
                        'default_con_type': 'engineering',
                        'is_contract': 1,
                        'search_default_not_finished': 1,
                        'search_default_con_type': 'engineering',
                        'default_contract_type': 'sale'},
            'domain': domain,
        }

    def get_subcontractor_payment(self):
        subcontractor_payment_ids = self.env['line.contract.installment'].search([('project_id', '=', self.id),
                                                                          ('payment_type', '=', 'contractor')])
        form_id = self.env.ref('khawald_project_contract.kh_project_contract_installment_form_view').id
        tree_id = self.env.ref('khawald_project_contract.kh_project_contract_installment_tree_view').id
        domain = [('id', 'in', subcontractor_payment_ids.ids)]
        return {
            'name': _('Contractor Payment'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'line.contract.installment',
            'views': [(tree_id, 'tree'), (form_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
        }

    def get_engineering_payment(self):
        engineering_payment_ids = self.env['line.contract.installment'].search([('project_id', '=', self.id),
                                                                                  ('payment_type', '=', 'engineering')])
        form_id = self.env.ref('khawald_project_contract.kh_project_contract_installment_form_view').id
        tree_id = self.env.ref('khawald_project_contract.kh_project_contract_installment_tree_view').id
        domain = [('id', 'in', engineering_payment_ids.ids)]
        return {
            'name': _('Engineering Payment'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'line.contract.installment',
            'views': [(tree_id, 'tree'), (form_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
        }


    def count_payment_number(self):
        spayment_count = self.env['line.contract.installment'].search_count([('project_id', '=', self.id),
                                                                           ('payment_type', '=', 'contractor')])
        epayment_count = self.env['line.contract.installment'].search_count([('project_id', '=', self.id),
                                                                           ('payment_type', '=', 'engineering')])

        self.spayment_counts = spayment_count
        self.epayment_counts = epayment_count

    def _check_validations(self):
        for record in self:
            if not record.eng_installment_line_ids:
                raise ValidationError(_("To Proceed,Please Insert Engineering Office Payment"))
            if record.eng_installment_line_ids:
                due_date = record.eng_installment_line_ids.mapped('due_date')
                if len(due_date) == 1 and not due_date[0]:
                    raise ValidationError(_("To Proceed,Please Insert Engineering Office Payment"))


class ProjectContract(models.Model):
    _inherit = 'contract.contract'
    _description = "Project Contract"

    project_id = fields.Many2one('project.project', string="Project")
    con_type = fields.Selection([('contractor', 'Contractor'),
                                ('engineering', 'Engineering')], string="Contract Type")
    def get_installment(self):
        form_view = self.env.ref('contract.contract_installment_form_view').id
        tree_view = self.env.ref('contract.contract_installment_tree').id

        return {
            'name': 'Contract Installment',
            'view_mode': 'tree, form',
            'res_model': 'line.contract.installment',
            'views': [
                (tree_view, 'tree'),
                (form_view, 'form')
            ],
            'type': 'ir.actions.act_window',
            'domain': [('contract_id', '=', self.id)],
            'context': {'default_contract_id':self.id ,'default_project_id': self.project_id.id, 'default_payment_type':self.con_type}
        }


class LineContractInstallment(models.Model):
    _inherit = "line.contract.installment"
    _description = "Installment Project"

    project_id = fields.Many2one('project.project', string="Project")
    payment_type = fields.Selection([('contractor', 'Contractor'),
                                     ('engineering', 'Engineering')], string="Payment Type")


