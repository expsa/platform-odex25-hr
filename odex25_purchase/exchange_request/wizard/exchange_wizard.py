# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from dateutil import relativedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError, AccessError, UserError


class TransportMethodWizard(models.TransientModel):
    _name = 'exchange.wizard'

    exchange_id = fields.Many2one('exchange.request')
    name = fields.Char(related="exchange_id.name")
    line_ids = fields.Many2many('exchange.wizard.line', 'wizard_id')

    def print_report(self):

        """
            create picking
        """
        move_lines = []
        if self.exchange_id.stock_journal_id.location_id.id == False:
            raise ValidationError(_("Please Select a location in your stock journal first"))
        if self.exchange_id.requisition_type == 'exchange':
            source = self.exchange_id.location_id.id
            dest = self.exchange_id.stock_journal_id.location_id.id
        else:
            source = self.exchange_id.stock_journal_id.location_id.id
            dest = self.exchange_id.location_id.id
        print(self.line_ids)
        for rec in self.line_ids:
            result = rec.picking_done + rec.picking_quantity
            quant = rec.product_qty
            if result > quant:
                raise ValidationError(_("Pickgin Quantity Can't be more than Asked Quantity"))
            if rec.product_id.type != 'service':
                move_lines.append((0, 0, {
                    'name': rec.product_id.name,
                    'product_id': rec.product_id.id,
                    'product_uom_qty': rec.qty_available,
                    'product_uom': rec.Uom_id.id,
                    'location_dest_id': dest,
                }))
        if len(move_lines) != 0:
            stock_picking = self.env['stock.picking'].create({
                'name': 'mosabtest',
                'date': self.exchange_id.request_date,
                'partner_id': self.exchange_id.user_id.partner_id.id,
                'origin': self.exchange_id.name,
                'department_id': self.exchange_id.department_id.id,
                'category_id': self.exchange_id.category_id.id,
                'picking_type_id': self.exchange_id.picking_type_id.id,
                'location_dest_id': dest,
                'location_id': source,
                'state': 'assigned',
                'move_lines': move_lines,
            })
            for rec in stock_picking.move_lines:
                rec._set_quantity_done(rec.product_qty)
            self.exchange_id.write({'stock_picking': [(4, stock_picking.id)]})
            state = True
            for rec in self.line_ids:
                result = rec.picking_done + rec.picking_quantity
                quant = rec.product_qty
                if result != quant:
                    state = False
            if state:
                self.exchange_id.write({'state': 'done'})
        return True


class TransportMethodWizard(models.TransientModel):
    _name = 'purchase.wizard'

    exchange_id = fields.Many2one('exchange.request')
    name = fields.Char(related="exchange_id.name")
    line_ids = fields.Many2many('exchange.wizard.line', 'purchase_wizard_id')

    def print_report(self):
        """
            create picking
        """
        picktype = False
        if self.exchange_id.type != 'service':
            if self.exchange_id.requisition_type == 'exchange':
                picktype = self.env['stock.picking.type'].search(
                    [('warehouse_id', '=', self.exchange_id.warehouse_id.id), ('code', '=', 'incoming')])[0].id
            if self.exchange_id.requisition_type == 'return':
                picktype = self.env['stock.picking.type'].search(
                    [('warehouse_id', '=', self.warehouse_id.exchange_id.id), ('code', '=', 'outgoing')])[0].id
        if len(self.exchange_id.requisition_id) != 0:
            if self.exchange_id.requisition_id.state != 'cancel':
                raise ValidationError(_("This Request already have Purchase Requisition"))
        else:
            move_lines = []
            for rec in self.line_ids:
                move_lines.append((0, 0, {
                    'product_id': rec.product_id.id,
                    'qty': rec.product_qty - rec.qty_available,
                    'name': rec.note,
                    'price_unit': 0
                }))
            purchase_request = self.env['purchase.request'].create({
                # 'name':self.name,
                # 'exchange_date':self.exchange_id.request_date,
                # 'priority':self.exchange_id.priority,
                'product_category_ids': [(6, 0, self.exchange_id.category_ids.ids)],
                'department_id': self.exchange_id.department_id.id,
                'purchase_purpose': self.exchange_id.purpose,
                "type": self.exchange_id.purchase_type,
                # 'origin': self.exchange_id.name,
                # 'stock_journal_id':self.exchange_id.stock_journal_id.id,
                'picking_type_id': picktype,
                'state': 'draft',
                'exchange_request': self.exchange_id.id,
                'line_ids': move_lines,
                # 'vendor_ids': [(4, vendor.id, None) for vendor in self.exchange_id.vendor_ids],
                # 'justification':self.exchange_id.justification,
            })
            self.exchange_id.request_id = purchase_request
            self.exchange_id.write({'state': 'waiting'})


class ExchangeLines(models.TransientModel):
    _name = 'exchange.wizard.line'

    wizard_id = fields.Many2one('exchange.wizard')
    purchase_wizard_id = fields.Many2one('purchase.wizard')
    requ_name = fields.Char(related="wizard_id.name", store=True)
    purchase_requ_name = fields.Char(related="purchase_wizard_id.name", store=True)
    product_id = fields.Many2one('product.product')
    name = fields.Char(related='product_id.name')
    product_qty = fields.Integer()
    Uom_id = fields.Many2one(related='product_id.uom_id')
    note = fields.Char()
    qty_available = fields.Float()
    picking_quantity = fields.Integer()
    picking_done = fields.Integer()


class ExchangePartialLines(models.TransientModel):
    _name = 'partial.exchange'

    exchange_id = fields.Many2one(comodel_name='exchange.request', string='')
    partial_lines = fields.Many2many('exchange.request.line')

    def action_close(self):
        for line in self.partial_lines:
            if line.qty_available == 0:
                line.unlink()
                continue
            line.product_qty = line.qty_available
        self.exchange_id.write({'state': 'sign'})

    def action_purchase(self):
        return self.exchange_id.action_purchase_request_wizard()
