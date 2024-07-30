# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    second_approve = fields.Integer(string='second approve')
    # third_approve = fields.Integer(string='third approve')
    purchase_budget = fields.Boolean(string='Purchase budget')
    purchase_analytic_account = fields.Many2one('account.analytic.account')
#     todo start
#     add new purchase setting
    exceptional_amount = fields.Float(string='Exceptional Amount',)
    chief_executive_officer = fields.Float(string='Exceptional Amount',)
    direct_purchase = fields.Float(string='Direct Purchase Amount',)
# todo end
