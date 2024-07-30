# -*- coding: utf-8 -*-
import base64
import re
import calendar

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import exception_to_unicode
from odoo import models, fields, api, exceptions, tools, _
from odoo.addons.property_management.models import amount_to_text_ar


class RentPayment(models.Model):
    _name = "rent.payment"
    _description = "Rental Contract Payment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    code = fields.Char(string="Sequence")
    name = fields.Char(string="Description")
    contract_id = fields.Many2one('rental.contract', string="Rental Contract")
    investor_id = fields.Many2one('res.partner', string="Investor", related="contract_id.property_id.owner_id",
                                  store=True)
    partner_id = fields.Many2one('res.partner', string="Customer", related="contract_id.partner_id", store=True)
    property_id = fields.Many2one('internal.property', string="Property", related="contract_id.property_id", store=True)
    unit_ids = fields.Many2many('re.unit', string="Unit/Units", related="contract_id.unit_ids")
    user_id = fields.Many2one('res.users', string="Responsible")
    company_id = fields.Many2one('res.company', string="Company")
    due_date = fields.Date(string="Due Date")
    paid_date = fields.Date(string="Paid Date")
    payment_method = fields.Selection([('check', 'Bank Check'),
                                       ('cash', 'Cash'),
                                       ('transfer', 'Transfer')], string="Payment Method", default='transfer')
    amount = fields.Float(string="Amount")
    water_cost = fields.Float(string="Water Cost")
    service_cost = fields.Float(string="Service Cost")
    profit = fields.Float(string="Profit")
    tax_id = fields.Many2one('account.tax', string="Tax")
    untaxed_amount = fields.Float(string="Untaxed Amount", compute="get_untaxed_amount", store=True)
    # tax_amount = fields.Float(string="Tax Amount", compute="get_tax_amount", store=True)
    tax_amount = fields.Float(string="Tax Amount")
    total_amount = fields.Float(string="Total Amount", compute="get_total_amount")
    paid = fields.Boolean(string="Paid", compute='get_invoice_state', default=False)
    amount_in_word = fields.Char(string="Amount In Word", compute="get_amount_in_word")
    state = fields.Selection([('draft', 'Not Due'),
                              ('due', 'Due'),
                              ('paid', 'Paid'),
                              ('cancel', 'Canceled')], string="Status", default='draft')
    invoice_id = fields.Many2one('account.move', string="Invoice")
    note = fields.Text(string="Note")

    @api.depends('invoice_id', 'invoice_id.state', 'invoice_id.amount_residual')
    def get_invoice_state(self):
        self.paid = False
        for rec in self:
            if rec.invoice_id:
                if rec.invoice_id.amount_residual == 0.0:
                    rec.paid = True


    def _prepare_invoice_values(self, payment, amount):
        invoice_vals = {
            'ref': payment.name,
            'move_type': 'out_invoice',
            'invoice_origin': payment.code,
            'invoice_user_id': payment.user_id.id,
            'narration': payment.note,
            'partner_id': payment.contract_id.partner_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': payment.name + ' - ' + payment.code + ' - ' + str(payment.due_date),
                'price_unit': amount,
                'quantity': 1.0,
                'account_id': payment.contract_id.accrued_account_id.id,
                # 'tax_ids': [(6, 0, [payment.tax_id.id])],
            })],
        }
        return invoice_vals

    def action_invoice(self):
        if not self.contract_id.accrued_account_id:
            raise exceptions.ValidationError(_("Kindly, Contact Your Account Manager to set Income Account in contract account page"))
        invoice_vals = self._prepare_invoice_values(self, self.total_amount)
        invoice = self.env['account.move'].sudo().create(invoice_vals).with_user(self.env.uid)
        self.invoice_id = invoice.id
        self.write({'state': 'paid'})

    @api.depends('total_amount')
    def get_amount_in_word(self):
        self.amount_in_word = amount_to_text_ar.amount_to_text(
            self.total_amount, 'ar')

    def action_cancel(self):
        if self.state != 'due':
            self.write(({'state': 'cancel'}))
        elif self.state == 'due':
            raise exceptions.ValidationError(_('Cannot Cancel This Payment Because it Due'))

    def action_validate(self):
        if self.contract_id.state == 'confirm':
            rent_payment = [line for line in self.contract_id.rent_payment_ids.filtered(
                lambda payment: payment.due_date < self.due_date and
                                (not payment.invoice_id or
                                 all(invoice.state == 'draft' for invoice in payment.invoice_id))
            )]
            if len(rent_payment):
                raise exceptions.ValidationError(
                    _("You must validate the previous rent payment and complete the process"))
            if self.code == '/' or not self.code:
                code = self.env['ir.sequence'].next_by_code('rent.payment') or '/'
                self.write({'code': code})
            self.write({"state": 'due'})
        else:
            raise exceptions.ValidationError(_("You Must Confirm Contract First"))

    # @api.depends('untaxed_amount', 'tax_id', 'tax_id.amount')
    # def get_tax_amount(self):
    #     for rec in self:
    #         tax_value = rec.tax_id.amount / 100
    #         rec.tax_amount = rec.untaxed_amount * tax_value

    @api.depends('amount', 'water_cost', 'service_cost')
    def get_untaxed_amount(self):
        for rec in self:
            rec.untaxed_amount = rec.amount + rec.water_cost + rec.service_cost

    @api.depends('amount', 'water_cost', 'service_cost')
    def get_total_amount(self):
        for rec in self:
            rec.total_amount = rec.amount + rec.water_cost + rec.service_cost
