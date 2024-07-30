
# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import UserError


class CrossoveredBudgetCustom(models.Model):
    _inherit = 'crossovered.budget.lines'

    @api.constrains('analytic_account_id')
    def _constrains_analytic_account_id(self):
        for rec in self:
            analytic_account_id = self.env['crossovered.budget.lines'].search(
                [('analytic_account_id', '=', rec.analytic_account_id.id), ('date_from', '<=', rec.date_from), ('date_to', '<=', rec.date_to),])
            if len(analytic_account_id) > 1:
                raise UserError(_("This analytic account account is already exit"))
