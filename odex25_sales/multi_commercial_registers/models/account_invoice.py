# -*- coding: utf-8 -*-
from odoo import models, fields, _

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    print_by_branch = fields.Boolean('Invoice with Branch', default=True)
