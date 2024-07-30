# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.move"

    discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')])
    discount_rate = fields.Float(digits='Discount')

    @api.onchange('discount_type', 'discount_rate', 'invoice_line_ids')
    def set_lines_discount(self):
        for move in self:
            discount_rate = move._get_discount_rate()
            previous_discount_rate = move._origin._get_discount_rate()
            if discount_rate == previous_discount_rate:
                for line in move.invoice_line_ids:
                    line.discount += discount_rate
            else:
                for line in move.invoice_line_ids:
                    discount = line._origin.discount
                    discount -= previous_discount_rate
                    discount += discount_rate
                    line.discount = discount

            move.line_ids._onchange_price_subtotal()
            move._onchange_invoice_line_ids()
            move._compute_invoice_taxes_by_group()
                
    def _get_discount_rate(self):
        discount_rate = 0
        if self.discount_type == 'amount':
            move_total = sum(self.invoice_line_ids.mapped(lambda l: l.quantity * l.price_unit))
            discount_rate = (self.discount_rate / (move_total or 1)) * 100
        elif self.discount_type == 'percent':
            discount_rate = self.discount_rate
        return discount_rate

    


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    discount = fields.Float(digits='Total Discount')
