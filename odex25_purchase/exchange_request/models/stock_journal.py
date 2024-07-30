# -*- coding: utf-8 -*-

from odoo import fields, models, _


class StockJournal(models.Model):
    _name = 'stock.journal'

    name = fields.Char(required=True)
    location_id = fields.Many2one('stock.location')
    exchange = fields.Boolean()
    analytic_account_id = fields.Many2one('account.analytic.account')
