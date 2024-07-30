# -*- coding: utf-8 -*-
import base64
import re
import calendar

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import exception_to_unicode
from odoo import models, fields, api, exceptions, tools, _


_logger = logging.getLogger(__name__)


class RentalContractTemplate(models.Model):
    _name = 'rental.contract.template'

    name = fields.Char(string="Template Name")
    template = fields.Html(string="Template")


class Property(models.Model):
    _inherit = "internal.property"

    action_type = fields.Selection(selection_add=[('rent', 'Rent')])

    

class ResUnit(models.Model):
    _inherit = "re.unit"

    action_type = fields.Selection(selection_add=[('rent', 'Rent')])
    contract_id = fields.Many2one('rental.contract', string="Rental Contract")

    contract_counts = fields.Integer(string='Contracts', compute='count_contracts_number')

    def count_contracts_number(self):
        contract_count = self.env['rental.contract'].search([('unit_ids', '=', self.id)])
        self.contract_counts = len(contract_count)

    def get_contract(self):
        contract_id = self.env['rental.contract'].search(
            [('unit_ids', '=', self.id)])
        form_id = self.env.ref('property_management.rental_contract_form_view').id
        list_id = self.env.ref('property_management.rental_contract_list_view').id
        domain = [('id', 'in', contract_id.ids)]
        return {
            'name': _('Rental Contract'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'rental.contract',
            'views': [(list_id, 'tree'), (form_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
        }


class RentalContract(models.Model):
    _name = 'rental.contract'
    _description = 'Rental Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    @api.onchange('rent_method')
    def onchange_rent_method(self):
        """
        Based on rent method return the following record
        to double check in xml domain in unit that only available
        :return: if property return the approved property
        :return: else return the available unit of approved property
        """
        if self.rent_method and self.rent_method == 'property':
            property_ids = self.env['internal.property'].sudo().search(
                [('state', '=', 'approve'), ('action_type', '=', 'rent')])
            return {'domain': {'property_id': [('id', 'in', property_ids.ids)]}}
        elif self.rent_method and self.rent_method == 'unit':
            if not self.property_id:
                self.property_id = False
            property_ids = self.env['internal.property'].sudo().search(
                [('state', '=', 'approve'), ('action_type', '=', 'rent')])
            print()
            property_list = property_ids.filtered(
                lambda line: len(line.unit_ids) > 0 and any(unit.state == 'available' for unit in line.unit_ids))
            return {'domain': {'property_id': [('id', 'in', property_list.ids)]}}
        else:
            if not self.property_id:
                self.property_id = False

    active = fields.Boolean(default=True)
    name = fields.Char(string="Name")
    date = fields.Date(string="Contract Date")
    seq = fields.Char(string="Sequence", default="/",index=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('submit', 'Submit'),
                              ('review', 'Review'),
                              ('confirm', 'Confirmed'),
                              ('renewed', 'Renewed'),
                              ('cancel', 'Cancelled'),
                              ('close', 'Closed')], string='Status',
                             default='draft', track_visibility='always')
    residential_purpose_id = fields.Many2one('residential.purpose', string="Residential Purpose")
    rent_method = fields.Selection([('property', 'Property'),
                                    ('unit', 'Unit')], string="Rent Method")
    property_id = fields.Many2one('internal.property', string="Property",track_visibility='always')
    unit_ids = fields.Many2many('re.unit', string="Units",track_visibility='always')
    partner_id = fields.Many2one('res.partner', string="Renter")
    identification_type = fields.Selection(related="partner_id.identification_type", string='Identification Type')
    identification_number = fields.Char(related="partner_id.identification_number", string='Identification NUmber')
    identification_issue_date = fields.Date(related="partner_id.identification_issue_date", string='Identification Issue Date')
    identification_expiry_date = fields.Date(related="partner_id.identification_expiry_date", string='Identification Expiry Date')

    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user.id)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    rent_duration = fields.Integer(string="Rent Duration", default=1)
    rent_kind = fields.Selection([('year', 'Year'),
                                  ('month', 'Month'),
                                  ], string="Rent Kind", track_visibility='always')
    date_from = fields.Date(string="Rent Date from", default=fields.Date.today)
    date_to = fields.Date(string="Rent Date To", compute="get_to_date", store=True)
    # separate_service = fields.Boolean(string="Separate Service ?")
    rent_type = fields.Many2one('rent.type', string="Rent Type")
    space = fields.Float(string="Space", compute="get_property_unit_space", store=True)
    service = fields.Selection([('fixed', 'Fixed'), ('percentage', 'Percentage')], string="Service")
    service_cost = fields.Float(string="service cost")
    service_amount = fields.Float(string="service amount", compute="compute_service_amount", store=True)
    management_type = fields.Selection(related="property_id.management_type", string="Management Type")
    property_state_id = fields.Many2one('re.property.state', related="property_id.property_state_id")
    property_type_id = fields.Many2one('internal.property.type', related="property_id.property_type_id", string="Type")
    market_type = fields.Selection(related="property_id.market_type", string="Market Type")
    city_id = fields.Many2one('re.city', related="property_id.city_id", string="City")
    district_id = fields.Many2one('district', related="property_id.district_id", string="District")
    street = fields.Char(string="Street Name", related="property_id.street")
    check_insurance = fields.Boolean(string='Insurance?', default=False)
    meter_price = fields.Float(string='Price Per Meter', compute="unit_property_meter_price", store=True)
    cal_rent_amount = fields.Float(string='Calculated Rent Amount',compute="get_rent_amount", store=True)
    rent_amount = fields.Float(string='Rent Amount')
    original_rent_amount = fields.Float(string='Rent Amount')
    insurance = fields.Selection([('fixed', 'Fixed'),
                                  ('percentage', 'Percentage')], string="Insurance", default="fixed")
    insurance_cost = fields.Float(string="Insurance cost")
    insurance_amount = fields.Float(string="Insurance Amount", compute="compute_insurance", store=True)
    insurance_paid = fields.Float(string="Insurance Paid",compute="get_insurance_Paid", store=True)
    is_services = fields.Boolean(string='Services Exist?', copy=False)
    water_meter_no = fields.Char(string='Water Meter No.')
    electricity_meter_no = fields.Char(string='Electricity Meter No.')
    generated = fields.Boolean(string='Generated')
    closed = fields.Boolean(string='Closed')
    annual_raise_ids = fields.One2many('annual.raise', 'contract_id', string='Annual Raise', copy=False)
    rent_payment_ids = fields.One2many('rent.payment', 'contract_id', string="Rent Payment")
    insurance_invoice_id = fields.Many2one('account.move',string="Insurance Invoice")
    external_broker = fields.Boolean(string="External Broker")
    external_broker_id = fields.Many2one('res.partner', string="External Broker")
    external_percent = fields.Float(string="External Broker Percent")
    external_commission = fields.Float(string="External Broker Commission")
    internal_broker = fields.Boolean(string="Internal Broker")
    internal_broker_id = fields.Many2one('res.partner', string="Internal Broker")
    internal_percent = fields.Float(string="Internal Broker Percent")
    internal_commission = fields.Float(string="Internal Broker Commission")
    renter_commission = fields.Boolean(string="Renter Commission")
    renter_percent = fields.Float(string="Renter Commission Percent")
    renter_value = fields.Float(string="Renter Value")
    journal_id = fields.Many2one('account.journal', string="Journal")
    debit_account_id = fields.Many2one('account.account', string="Debit Account")
    accrued_account_id = fields.Many2one('account.account', string="Accrued Account")
    revenue_account_id = fields.Many2one('account.account', string="Revenue Account")
    note = fields.Html(string="Note")
    water_cost = fields.Float(string="Water Cost")
    template_id = fields.Many2one('rental.contract.template', string="Rental Contract Template")
    template = fields.Html(string="Template")
    commission_profit = fields.Selection([('percentage', "Percentage"),
                                          ('number', "Fixed")], string='Commission', copy=False)
    company_profit = fields.Selection([('percentage', 'Percentage'), ('number', 'Fixed amount')],
                                      string='Company Profit')
    company_profit_amount = fields.Float(string='Company Profit Amount')
    company_profit_val = fields.Float(string='Company Profit', compute='_compute_company_profit_val', store=True)
    change_price = fields.Boolean(string='Do You want to change rent?', default=False)
    new_price = fields.Float(string="New Meter Price")
    new_rent_amount = fields.Float(string='New Rent Amount', copy=False, track_visibility='always')
    renew_contract_id = fields.Many2one('rental.contract', string='New Contract')
    renew_done = fields.Boolean(string='Renew Completed', default=False)
    renewed = fields.Boolean(string='Renewed Contract', default=False)
    previous_contract_id = fields.Many2one('rental.contract', string='Previous Contract')
    log_rental_contract_ids = fields.One2many('log.rental.contract','contract_id', string='Contract')
    annual_raise_on_type = fields.Selection([('meter', _('Meter')), ('rent_amount', _('Rent amount'))],
                                            _('الزيادة علي'), default='rent_amount')

    def action_renew(self):
        """
        Renew the contract and link the previous contract to the new one
        change the state of contract to renewed
        :return:
        """
        # ToDo: when invoicing is done link the previous created invoice of insurance
        flag = True
        for payment in self.rent_payment_ids:
            if payment.state not in ['paid', 'cancel']:
                flag = False
        if not flag:
            raise exceptions.ValidationError(
                _("Renewing process cannot be completed please check the rent payment status"))
        if flag:
            contract_values = {
                'state': 'draft',
                'name': self.name,
                'rent_method': self.rent_method,
                'property_id': self.property_id.id,
                'unit_ids': [(4, unit.id) for unit in self.unit_ids],
                'user_id': self.env.user.id,
                'date_from': self.date_to,
                'rent_duration': self.rent_duration,
                'rent_kind': self.rent_kind,
                'partner_id': self.partner_id.id,
                'rent_type': self.rent_type.id,
                'rent_amount': self.rent_amount,
                'water_cost': self.water_cost,
                'services_cost': self.service_amount,
                'service_cost': self.service_cost,
                'previous_contract_id': self.id,
                'insurance_cost': self.insurance_cost,
                'insurance_amount': self.insurance_amount,
                'insurance_paid': self.insurance_paid,
                'insurance_calculation_method': self.insurance_calculation_method,
                'insurance': self.insurance,
            }
            renewed_contract_id = self.env['rental.contract'].create(contract_values)
            for rec in self.unit_ids:
                rec.write({'state': 'available'})
            self.write({'renew_contract_id': renewed_contract_id.id,
                        'renewed': True,
                        'state': 'renewed'
                        })


    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        raise exceptions.ValidationError(_("Cannot Duplicate The Contractr"))

    @api.onchange('change_price')
    def set_change_price(self):
        if not self.change_price:
            self.new_price = 0.0
            self.rent_amount = 0.0


    @api.depends('company_profit', 'company_profit_amount')
    def _compute_company_profit_val(self):
        for record in self:
            if record.company_profit and record.company_profit == 'percentage':
                record.company_profit_val = record.company_profit_amount / 100 * record.rent_amount
            elif record.company_profit and record.company_profit == 'number':
                record.company_profit_val = record.company_profit_amount
            else:
                record.company_profit_val = 0.0



    @api.constrains('unit_id')
    def check_unit_state(self):
        for unit in self.unit_ids:
            if unit.state != 'available':
                raise exceptions.ValidationError(_("Unit %s is not available") %
                                                 (unit.name))
            else:
                pass

    @api.onchange('template_id')
    def onchange_template(self):
        self.template = self.template_id.template

    @api.depends('insurance_invoice_id','insurance_invoice_id.amount_residual', 'insurance_amount')
    def get_insurance_paid(self):
        if self.insurance_invoice_id:
            residual = self.insurance_invoice_id.amount_residual
            self.insurance_paid = residual if residual != 0.0 else self.insurance_amount

    def _prepare_invoice_values(self, contract, amount):
        invoice_vals = {
            'ref': _("Insurance payment for ")+contract.name,
            'move_type': 'out_invoice',
            'invoice_origin': contract.seq,
            'invoice_user_id': contract.user_id.id,
            'narration': contract.note,
            'partner_id': contract.partner_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': contract.name + ' - ' + contract.seq + ' - ' + str(contract.date),
                'price_unit': amount,
                'quantity': 1.0,
                'account_id':contract.journal_id.default_account_id.id

            })],
        }
        return invoice_vals

    def action_confirm(self):
        invoice_vals = self._prepare_invoice_values(self, self.insurance_amount)
        invoice = self.env['account.move'].sudo().create(invoice_vals).with_user(self.env.uid)
        self.insurance_invoice_id = invoice.id
        if self.rent_method != 'property':
            for unit in self.unit_ids:
                unit.write({'state': 'rented',
                            'contract_id': self.id})

        elif self.rent_method == 'property':
            for unit in self.property_id.unit_ids:
                unit.write({'state': 'rented',
                            'contract_id': self.id})
            self.property_id.write({'state': 'rent'})
        self.env['log.rental.contract'].create({'contract_id': self.id,
                                                'leaser_id': self.partner_id.id,
                                                'date_start': self.date_from,
                                                'date_end': self.date_to})
        self.write({'state': 'confirm'})

    def action_review(self):
        full = True
        if self.property_id.state in ['reserve', 'rent']:
            raise exceptions.ValidationError(_("Property is already reserved or rented"))
        for units in self.property_id.unit_ids:
            if units.state in ['draft', 'available']:
                full = False
        if full:
            self.property_id.write({'state': 'rent'})
        total_rent = round(self.cal_rent_amount * self.rent_duration, 2)
        total_service = round(self.service_amount * self.rent_duration, 2)
        total_water = round(self.water_cost * self.rent_duration, 2)
        rent_payment = round(sum([rent.amount for rent in self.rent_payment_ids]), 2)
        service_payment = round(sum([rent.service_cost for rent in self.rent_payment_ids]), 2)
        water_payment = round(sum([rent.water_cost for rent in self.rent_payment_ids]), 2)

        if total_rent != rent_payment and not self.annual_raise_ids:
            raise exceptions.ValidationError(
                _("Rent payment %s is not equal the rent total amount %s ") % (rent_payment, total_rent))
        if total_service != service_payment:
            raise exceptions.ValidationError(
                _("Service payment %s is not equal the rent total service amount %s ") % (
                service_payment, total_service))
        if total_water != water_payment:
            raise exceptions.ValidationError(
                _("Water cost to pay %s is not equal the rent total water cost %s ") % (water_payment, total_water))
        self.write({'state': 'review'})

    def action_submit(self):
        self.seq = self.env['ir.sequence'].next_by_code('rental.contract') or '/'
        if not self.rent_payment_ids:
            self.generate_payments()
        if self.rent_method != 'property':
            for unit in self.unit_ids:
                if unit.state != 'available':
                    raise exceptions.ValidationError(_("Unit %s is not available") %
                                                     (unit.name))
                else:
                    unit.write({'state': 'reserved',
                                'contract_id': self.id})
        elif self.rent_method == 'property':
            for unit in self.property_id.unit_ids:
                unit.write({'state': 'reserved',
                            'contract_id': self.id})
            self.property_id.write({'state': 'reserve'})
        self.write({'state': 'submit'})

    @api.depends('insurance', 'insurance_cost', 'cal_rent_amount')
    def compute_insurance(self):
        if self.insurance and self.insurance == 'percentage':
            self.insurance_amount = (self.insurance_cost / 100.0) * self.cal_rent_amount
        elif self.insurance and self.insurance == 'fixed':
            self.insurance_amount = self.insurance_cost

    def action_cancel(self):
        if self.rent_payment_ids:
            for payment in self.rent_payment_ids:
                if payment.state != 'paid':
                    payment.write({'state': 'cancel'})
        if self.rent_method != 'property':
            for unit in self.unit_ids:
                unit.write({'state': 'available'})
        elif self.rent_method == 'property':
            for unit in self.property_id.unit_ids:
                unit.write({'state': 'available',
                            'contract_id': self.id})
            self.property_id.write({'state': 'register'})
        self.write({'state': 'cancel'})

    @api.depends('service', 'service_cost', 'cal_rent_amount')
    def compute_service_amount(self):
        if self.service and self.service == 'percentage':
            self.service_amount = (self.service_cost / 100) * self.cal_rent_amount
        elif self.service and self.service == 'fixed':
            self.service_amount = self.service_cost

    @api.depends('rent_kind', 'meter_price', 'space', 'rent_amount', 'new_price', 'change_price')
    def get_rent_amount(self):
        """
        get total rent based on meter price and space rent kind
        :return:
        """
        rent_total = 0.0
        rent_price = self.meter_price
        if self.change_price and self.new_price > 0.0:
            rent_price = self.new_price
        if self.rent_kind == 'year':
            rent_total = (self.space * rent_price)
        if self.rent_kind == 'month':
            rent_total = (self.space * rent_price / 12)
        if self.rent_kind == 'day':
            date_from = datetime.strptime(datetime.strftime(self.date_from, '%Y-%m-%d'), "%Y-%m-%d")
            if calendar.isleap(date_from.year):
                rent_total = (self.space * rent_price / 366)
            elif not calendar.isleap(date_from.year):
                rent_total = (self.space * rent_price / 365)
        if self.rent_kind == 'hour':
            date_from = datetime.strptime(
                datetime.strftime(self.date_from, "%Y-%m-%d"), "%Y-%m-%d")
            if calendar.isleap(date_from.year):
                rent_total = (self.space * rent_price / 366) / 24
            elif not calendar.isleap(date_from.year):
                rent_total = (self.space * rent_price / 365) / 24
        self.cal_rent_amount = rent_total if self.rent_amount == 0.0 else self.rent_amount



    @api.depends('rent_method', 'property_id.meter_price', 'property_id', 'unit_ids')
    def unit_property_meter_price(self):
        """
        get meter price based on rent method
        :return: if property based on meter_price on property object
        :return: if unit get the total unit price of all selected unit
        """
        total_price = 0.0
        if self.rent_method == 'property':
            self.meter_price = self.property_id.meter_price
        else:
            for unit in self.unit_ids:
                total_price += unit.meter_price
            self.meter_price = total_price

    @api.depends('rent_method', 'property_id', 'unit_ids')
    def get_property_unit_space(self):
        """
        get space based on rent method
        :return: if property return property space
        :return: if unit or more than one unit read the sum of space uing for loop
        """
        total_space = 0.0
        if self.rent_method == 'property':
            self.space = self.property_id.property_space
        else:
            for unit in self.unit_ids:
                total_space += unit.space
            self.space = total_space


    @api.depends('date_from', 'rent_duration', 'rent_kind')
    def get_to_date(self):
        if self.date_from and self.rent_duration and self.rent_kind:
            date_from = datetime.strptime(datetime.strftime(self.date_from, '%Y-%m-%d'), '%Y-%m-%d').date()
            date_from = date_from - relativedelta(days=int(1))
            if self.rent_kind == 'year':
                date_to = date_from + relativedelta(years=int(self.rent_duration))
                self.date_to = date_to.strftime('%Y-%m-%d')
            elif self.rent_kind == 'month':
                date_to = date_from + relativedelta(months=int(self.rent_duration))
                self.date_to = date_to.strftime('%Y-%m-%d')

    def check_line(self):
        """
        if there is a rent line then raise a confirm box if true remove all previous line
        and call generate function
        :return:
        """
        if len(self.rent_payment_ids) > 0:
            ctx = self._context.copy()
            ctx.update({'rent_payment': True})
            return {
                'name': _('Confirm'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'confirm.wizard',
                'context': ctx,
                'target': 'new',
            }
        else:
            self.generate_payments()

    def remove_payment(self):
        """remove all payment line"""
        self._cr.execute('delete from rent_payment where contract_id =%s' % self.id)

    def generate_payments(self):
        """
        based on user selection system will prepare the rent payment scheduling
        and create a rent line
        new change service will be like rent payment
        :return:
        """
        property_id = self.property_id.id
        tax_id = 0
        date_from = datetime.strptime(datetime.strftime(self.date_from, '%Y-%m-%d'), '%Y-%m-%d').date()
        date_to = datetime.strptime(datetime.strftime(self.date_to, '%Y-%m-%d'), '%Y-%m-%d').date()
        months = int(self.rent_type.months)
        service_months = 12
        # tax_ids = self.env['account.tax'].search([('type_tax_use', '=', 'sale')], limit=1)
        # if not tax_ids:
        #     raise exceptions.ValidationError(_('To Proceed, You must have a sale tax role'))
        # for tax in tax_ids:
        #     tax_id = tax.id
        ################################# section 1 ################################
        names = []
        if self.unit_ids:
            for unit in self.unit_ids:
                names.append(unit.name)

        # the rent factor is used to get the number of payments
        # also to get the rent amount based on rent_kind as following
        rent_factor = 1.0
        if self.rent_kind == 'year':
            rent_factor = 12.0
        if not self.date_from or not self.date_to:
            raise exceptions.ValidationError(_('Please set the rent duration and start date'))
        if months == 0:
            raise exceptions.ValidationError(_("In rent type please make sure that the month number is more than 0"))
        ################################# section 2 generate lines of payment based on given information ############
        no_payments = (self.rent_duration * rent_factor) / months
        no_services_payment = (self.rent_duration * rent_factor) / service_months
        rent_amount_per_payment = self.cal_rent_amount / (rent_factor / months)
        water_amount_per_payment = self.water_cost / (rent_factor / service_months)
        services_amount_per_payment = self.service_amount / (rent_factor / service_months)
        date_from = datetime.strptime(datetime.strftime(self.date_from, '%Y-%m-%d'), '%Y-%m-%d').date()
        service_date_from = datetime.strptime(datetime.strftime(self.date_from, '%Y-%m-%d'), '%Y-%m-%d').date()
        next_date = date_from
        service_next_date = service_date_from
        payment = 0
        service = 0
        no_year = 1
        no_payment = 1
        # Service Fixed In Yearly Based
        while payment < no_payments:
            raise_line = [line for line in self.annual_raise_ids if
                          line.due_date_raise == next_date]
            if len(raise_line) > 0:
                amount = raise_line[0].rent_amount_after_raise
                rent_amount_per_payment = amount / (rent_factor / months)
            year = date_from.year
            self._cr.execute('INSERT INTO rent_payment \
                                                (name,contract_id,due_date,property_id, \
                          amount,water_cost,service_cost,user_id,company_id,state) \
                                                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
                             (
                                 str(_('Payment') + str(payment + 1)),
                                 str(self.id),
                                 str(date_from.strftime('%Y-%m-%d')),
                                 str(self.property_id.id),
                                 str(rent_amount_per_payment),
                                 '0.0',
                                 '0.0',
                                 str(self.user_id.id),
                                 str(self.env.user.company_id.id),
                                 str('draft'),
                                 ))
            if self.rent_kind in ['month', 'year']:
                next_date += relativedelta(months=months)
            if date_to > next_date:
                date_from = next_date
            # increase while loop by 1 to move forward
            payment += 1
        while no_services_payment > service and service_next_date <= date_to:
            # update query to set the value of service based on it date
            query = """update rent_payment set service_cost = %s, water_cost = %s where due_date = %s and contract_id = %s """
            self._cr.execute(query, (str(round(services_amount_per_payment, 2)),
                                     str(round(water_amount_per_payment, 2)),
                                     str(service_date_from.strftime('%Y-%m-%d')),
                                     str(self.id)))
            if self.rent_kind in ['month', 'year']:
                service_next_date += relativedelta(months=service_months)
            if date_to > service_next_date:
                service_date_from = service_next_date
            service += 1
        # TODO: Find a Proper Way To Solve The Problem
        for line in self.rent_payment_ids:
            # line.get_tax_amount()
            line.get_untaxed_amount()
            line.get_total_amount()
            ###################################### End of Generating Payment ############################


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = "Renter"

    is_renter = fields.Boolean(string="Renter")



class LogRentalContract(models.Model):
    _name = 'log.rental.contract'

    contract_id = fields.Many2one('rental.contract', string='Contract')
    leaser_id = fields.Many2one('res.partner', string='Leaser')
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')
