# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')])
    discount_rate = fields.Float(digits='Discount')
    
    @api.onchange('discount_type', 'discount_rate', 'order_line')
    def set_lines_discount(self):
        for order in self:
            discount_rate = order._get_discount_rate()
            previous_discount_rate = order._origin._get_discount_rate()
            if discount_rate == previous_discount_rate:
                for line in order.order_line:
                    line.discount += discount_rate
            else:
                for line in order.order_line:
                    discount = line._origin.discount
                    discount -= previous_discount_rate
                    discount += discount_rate
                    line.discount = discount
            
    @api.onchange('discount_rate')
    def _check_discount_rate(self):
        for order in self:
            if order.discount_rate < 0.0:
                raise UserError(_('Discount rate can\'t be less than 0'))
                
    def _get_discount_rate(self):
        discount_rate = 0
        if self.discount_type == 'amount':
            total = sum(self.order_line.mapped(lambda l: l.product_uom_qty * l.price_unit))
            discount_rate = (self.discount_rate / (total or 1)) * 100
        elif self.discount_type == 'percent':
            discount_rate = self.discount_rate
        return discount_rate

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'discount_type': self.discount_type,
            'discount_rate': self.discount_rate,
        })
        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    discount = fields.Float(digits='Total Discount')


class SaleOrderOption(models.Model):
    _inherit = "sale.order.option"

    discount = fields.Float(digits='Total Discount')
