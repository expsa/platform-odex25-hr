# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Company(models.Model):
    _inherit = "res.company"

    def reflect_code_prefix_change(self, old_code, new_code):
        accounts = self.env['account.account'].search([('code', 'like', old_code), ('internal_type', '=', 'liquidity'),
            ('company_id', '=', self.id)], order='code asc')
        for account in accounts:
            if old_code != False and account.code.startswith(old_code):
                account.write({'code': self.get_new_account_code(account.code, old_code, new_code)})

