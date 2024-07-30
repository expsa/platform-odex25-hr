# -*- coding: utf-8 -*-
import datetime
from odoo.exceptions import ValidationError
from odoo import api, fields, models, _
from datetime import datetime


class ExchangeRequest(models.Model):
    _name = 'exchange.request'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def get_default_employee_id(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)

    name = fields.Char()
    request_date = fields.Date(default=datetime.now())
    type = fields.Selection([('product', 'Product')], default='product')
    purpose = fields.Char()
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user.id)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)
    category_ids = fields.Many2many('product.category')
    location_id = fields.Many2one('stock.location')
    picking_type_id = fields.Many2one('stock.picking.type')
    requisition_id = fields.Many2one('purchase.requisition')
    request_id = fields.Many2one('purchase.request')
    line_ids = fields.One2many('exchange.request.line', 'exchange_id')
    partner_id = fields.Many2one('res.partner', default=lambda self: self.env.user.partner_id.id)
    reference = fields.Char()
    purchase_type = fields.Selection(invisible=True, default="operational")
    employee_id = fields.Many2one(comodel_name='hr.employee', default=get_default_employee_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('direct_manager', 'Department Manager'),
        ('confirm', 'Responsible Department'),
        ('sign', 'Sign'),
        ('waiting', 'Waiting For Purchase'),
        ('to_deliver', 'Waiting Delivery'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], default='draft', track_visibility='always')
    stock_journal_id = fields.Many2one('stock.journal')
    warehouse_id = fields.Many2one('stock.warehouse')
    stock_picking = fields.Many2many('stock.picking')
    requisition_type = fields.Selection([
        ('exchange', 'Exchange'),
        ('return', 'Return')
    ])
    department_id = fields.Many2one('hr.department', related="employee_id.department_id")
    request_id_count = fields.Integer(compute='_compute_request_number', string='Number of Purchase Requests')
    purchase_type = fields.Selection([('project', 'Project'), ('operational', 'Operational')], default="operational")
    other_employee = fields.Boolean('For Other Employee')

    return_exchange_id = fields.Many2one(
        string='Exchange',
        comodel_name='exchange.request',
    )

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.employee_id and self.requisition_type == 'return':
            return {
                'value': {'return_exchange_id': False},
                'domain': {
                    'return_exchange_id': [('employee_id', '=', self.employee_id.id),
                                           ('requisition_type', '=', 'exchange'), ('state', '=', 'done')]
                }
            }

    @api.onchange('return_exchange_id')
    def onchange_return_exchange_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            if rec.return_exchange_id:
                rec.category_ids = rec.return_exchange_id.category_ids
                for line in rec.return_exchange_id.line_ids:
                    vals = {
                        'product_id': line.product_id.id,
                        'note': line.note,
                        'product_qty': line.product_qty,
                        'Uom_id': line.Uom_id,
                    }
                    lines.append((0, 0, vals))
                rec.line_ids = lines

    @api.depends('request_id')
    def _compute_request_number(self):
        for exchange in self:
            exchange.request_id_count = len(exchange.request_id)

    @api.onchange('category_ids', 'type')
    def UnlinkLines(self):
        """
            this function is to discard line when changing the category
        """
        self.line_ids = False

    def action_submit(self):
        self.state = 'direct_manager'

    def unlink(self):
        for rec in self:
            if rec.state not in ('draft'):
                raise ValidationError(_('Sorry! You Cannot Delete not Draft Document .'))
        return super(ExchangeRequest, self).unlink()

    def copy(self, default=None):
        """
            To prevent creating requisition_id when duplicate the request
        """
        self.ensure_one()
        default = dict(default or {})
        default['requisition_id'] = False
        default['warehouse_id'] = False
        default['stock_picking'] = False
        default['category_ids'] = False
        default['location_id'] = False
        default['picking_type_id'] = False
        default['stock_journal_id'] = False
        default['department_id'] = False
        default['partner_id'] = False
        default['vendor_ids'] = False
        default['justification'] = False
        default['purpose'] = False
        default['Uom_id'] = False
        return super(ExchangeRequest, self).copy(default=default)

    @api.model
    def get_seq_to_view(self):
        """
            Create the Sequence
        """
        sequence = self.env['ir.sequence'].search([('code', '=', self._name)])
        return sequence.sequence.number_next_actual

    @api.model
    def create(self, vals):
        """
            Set the created sequence to the name of the document
        """
        if self._context.get('default_requisition_type') == 'exchange':
            vals['name'] = self.env['ir.sequence'].next_by_code('exchange.request') or '/'
        else:
            vals['name'] = self.env['ir.sequence'].next_by_code('return.request') or '/'
        return super(ExchangeRequest, self).create(vals)

    @api.onchange('requisition_type')
    def StockJournalDomain(self):
        """
            Domaining stock journal based on the exchange type
        """
        if self.requisition_type == 'exchange':
            return {'domain': {'stock_journal_id': [('exchange', '=', True)]}}
        if self.requisition_type == 'return':
            return {'domain': {'stock_journal_id': [('exchange', '=', False)]}}

    @api.onchange('warehouse_id')
    def LocationDomain(self):
        """
            Domaining Location depending on the warehouse selected
        """
        locations = []
        if self.warehouse_id:
            picktype = self.env['stock.picking.type'].search([
                ('code', '=', 'outgoing'),
                ('warehouse_id', '=', self.warehouse_id.id)
            ])
            for ptype in picktype:
                locations.append(ptype.default_location_src_id.id)
            if self.requisition_type == 'exchange':
                picktype = self.env['stock.picking.type'].search([
                    ('code', '=', 'outgoing'),
                    ('warehouse_id', '=', self.warehouse_id.id)
                ], limit=1)[0]
                self.picking_type_id = picktype.id
                location = picktype.default_location_src_id.id
                self.location_id = location
            if self.requisition_type == 'return':
                picktype = self.env['stock.picking.type'].search([
                    ('code', '=', 'incoming'),
                    ('warehouse_id', '=', self.warehouse_id.id)
                ], limit=1)[0]
                self.picking_type_id = picktype.id
                location = picktype.default_location_dest_id.id
        if len(locations) > 1:
            return {'domain': {'location_id': [('id', 'in', locations)]}}
        else:
            if len(locations) != 0:
                return {'domain': {'location_id': [('id', '=', locations[0])]}}

    @api.depends('warehouse_id')
    def GetPickingType(self):
        """
            Set Default Value For picking type
        """
        for rec in self:
            if rec.warehouse_id:
                if rec.requisition_type == 'exchange':
                    picktype = self.env['stock.picking.type'].search([
                        ('code', '=', 'outgoing'),
                        ('warehouse_id', '=', rec.warehouse_id.id)
                    ], limit=1)[0]
                    rec.picking_type_id = picktype.id

                    location = picktype.default_location_src_id.id
                    rec.location_id = location
                if rec.requisition_type == 'return':
                    picktype = self.env['stock.picking.type'].search([
                        ('code', '=', 'incoming'),
                        ('warehouse_id', '=', rec.warehouse_id.id)
                    ], limit=1)[0]
                    rec.picking_type_id = picktype.id
                    location = picktype.default_location_dest_id.id

    @api.onchange('location_id')
    def onchangeLocation(self):
        """
            This function calculate the available quantity in the specified location_id
        """
        for rec in self.line_ids:
            quantity = self.env['stock.quant'].search([
                ('product_id', '=', rec.product_id.id),
                ('location_id', '=', self.location_id.id),
            ])
            # if quantity != False:
            #     result = 0
            #     for rec in quantity:
            #         result += rec.quantity
            #     # rec.qty_available = result
            #     rec.write({'qty_available': result})
        if self.requisition_type == 'exchange':
            picktype = self.env['stock.picking.type'].search([
                ('warehouse_id', '=', self.warehouse_id.id),
                ('code', '=', 'outgoing'),
                ('default_location_src_id', '=', self.location_id.id)
            ])
            if len(picktype) != 0:
                self.picking_type_id = picktype[0].id
        if self.requisition_type == 'return':
            picktype = self.env['stock.picking.type'].search([
                ('warehouse_id', '=', self.warehouse_id.id),
                ('code', '=', 'incoming'),
                ('default_location_dest_id', '=', self.location_id.id)
            ])
            if len(picktype) != 0:
                self.picking_type_id = picktype[0].id

    def calculate(self):
        """
            This Function Calculate with the Magical Button in the view
        """
        for rec in self.line_ids:
            quantity = self.env['stock.quant'].search([
                ('product_id', '=', rec.product_id.id),
                ('location_id', '=', self.location_id.id),
            ])
            if quantity:
                result = 0
                for recc in quantity:
                    result += recc.quantity
                reserved = self._get_reserved(rec.product_id.id, self.location_id.id)
                rec.write({'qty_available': result - reserved})

    def _get_reserved(self, product_id, location_id):
        """
            this method locing for all reserved quantities for specific product
        """
        reserved = 0
        stock_moves = self.env['stock.move'].search([
            ('product_id', '=', product_id),
            ('location_id', '=', location_id),
            ('state', 'in', ['partially_available', 'assigned'])])
        for move in stock_moves:
            reserved += move.reserved_availability
        return reserved

    def action_confirm(self):
        """
            Move docuemtn to confirm state
        """
        if len(self.line_ids) == 0:
            raise ValidationError(_("Please add products before confirming your order"))
        self.write({'state': 'confirm'})

    def action_sign(self):
        """
            create stock move and move document to sign state
        """
        self.calculate()
        differ_lines = []
        for rec in self.line_ids:
            if self.requisition_type == 'exchange':
                if self.type != 'service':
                    if rec.qty_available <= 0:
                        raise ValidationError(_("Avialable Quantity can't be Zero or less"))
                    if rec.product_qty > rec.qty_available:
                        differ_lines.append(rec.id)
        if len(differ_lines) != 0:
            return {
                'name': _('Partial Delivery'),
                'type': 'ir.actions.act_window',
                'res_model': 'partial.exchange',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_exchange_id': self.id,
                    'default_partial_lines': differ_lines
                }
            }
        self.write({'state': 'sign'})

    def action_waiting(self):
        """
            Create Purchase Requisition and move document to waiting state
        """
        picktype = False
        if self.type != 'service':
            if self.requisition_type == 'exchange':
                picktype = self.env['stock.picking.type'].search(
                    [('warehouse_id', '=', self.warehouse_id.id), ('code', '=', 'incoming')])[0].id
            if self.requisition_type == 'return':
                picktype = self.env['stock.picking.type'].search(
                    [('warehouse_id', '=', self.warehouse_id.id), ('code', '=', 'outgoing')])[0].id
        if len(self.request_id) != 0:
            if self.request_id.state != 'cancel':
                raise ValidationError(_("This Request already have Purchase Request"))
        else:
            move_lines = []
            for rec in self.line_ids:
                move_lines.append((0, 0, {
                    'product_id': rec.product_id.id,
                    'product_qty': rec.product_qty,
                    'name': rec.note,
                }))
            purchase_request = self.env['purchase.request'].create({
                # 'name':self.name,
                'ordering_date': self.request_date,
                'origin': self.name,
                'picking_type_id': picktype,
                'state': 'draft',
                'exchange_request': self.id,
                'line_ids': move_lines,
            })
            self.request_id = purchase_request
            self.write({'state': 'waiting'})

    def action_purchase_request_list(self):
        """
            show the purchase request
        """
        return {
            'name': _('Purchase Request'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.request',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.request_id.id if self.request_id else False,
        }

    def action_done(self):
        """
            Move the document to done state
        """
        self.ensure_one()
        for rec in self:
            move_lines = []
            if not rec.stock_journal_id.location_id:
                raise ValidationError(_("Please Select a location in your stock journal first"))
            if rec.requisition_type == 'exchange':
                source = rec.location_id.id
                dest = rec.stock_journal_id.location_id.id
            else:
                source = rec.stock_journal_id.location_id.id
                dest = rec.location_id.id
            for line in rec.line_ids:
                if line.product_id.type != 'service':
                    move_lines.append((0, 0, {
                        'name': self.name,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_qty,
                        'product_uom': line.Uom_id.id,
                        'location_dest_id': dest,
                    }))
            if len(move_lines) != 0:
                stock_picking = self.env['stock.picking'].create({
                    'date': rec.request_date,
                    'partner_id': rec.user_id.partner_id.id,
                    'origin': rec.name,
                    #'category_id': rec.category_id.id,
                    'picking_type_id': rec.picking_type_id.id,
                    'location_dest_id': dest,
                    'location_id': source,
                    'state': 'assigned',
                    'product_type': rec.product_type,
                    'move_lines': move_lines,
                })
                for move in stock_picking.move_lines:
                    move._set_quantity_done(line.product_qty)
                rec.write({'stock_picking': [(4, stock_picking.id)]})
                # self.stock_picking = stock_picking.id
            rec.write({'state': 'to_deliver'})

    def action_cancel(self):
        """
            Move the document to cancel state
        """
        self.write({'state': 'cancel'})

    def GetSumOfDonePickgin(self, move_line):
        """
            accomulate all the done quantity in picking
        """
        result = 0
        if len(self.stock_picking) != 0:
            for rec in self.stock_picking:
                for line in rec.move_lines:
                    if line.product_id.id == move_line.product_id.id:
                        result += line.quantity_done
        return result

    def action_purchase_request_wizard(self):
        """this is creating purchase request wizard"""
        if self.request_id:
            if self.request_id.state != 'cancel':
                raise ValidationError(_("This Request already have Purchase Request"))
        self.calculate()
        lines = []
        for rec in self.line_ids:
            remain = rec.product_qty - self.GetSumOfDonePickgin(rec)
            if rec.product_qty > rec.qty_available:
                lines.append((0, 0, {
                    'name': rec.name,
                    'product_id': rec.product_id.id,
                    'product_qty': rec.product_qty,
                    'qty_available': rec.qty_available,
                    'Uom_id': rec.Uom_id.id,
                    'note': rec.note,
                    'picking_done': self.GetSumOfDonePickgin(rec),
                    'picking_quantity': remain,
                }))
        return {
            'name': _('Purchase Request Creation'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_exchange_id': self.id,
                'default_name': self.name,
                'default_line_ids': lines,
            }
        }

    def action_exchange_wizard(self):
        move_lines = []
        if not self.stock_journal_id.location_id:
            raise ValidationError(_("Please Select a location in your stock journal first"))
        if self.requisition_type == 'exchange':
            source = self.location_id.id
            dest = self.stock_journal_id.location_id.id
        else:
            source = self.stock_journal_id.location_id.id
            dest = self.location_id.id
        for rec in self.line_ids:
            if rec.product_id.type != 'service':
                move_lines.append((0, 0, {
                    'name': rec.product_id.name,
                    'product_id': rec.product_id.id,
                    'product_uom_qty': ((rec.product_qty > rec.qty_available) and rec.qty_available) or rec.product_qty,
                    'product_uom': rec.Uom_id.id,
                    'location_dest_id': dest,
                }))
        if len(move_lines) != 0:
            stock_picking = self.env['stock.picking'].create({
                'name': 'mosabtest',
                'date': self.request_date,
                'partner_id': self.user_id.partner_id.id,
                'origin': self.name,
                'department_id': self.department_id.id,
                'category_ids': self.category_ids.ids,
                'picking_type_id': self.picking_type_id.id,
                'location_dest_id': dest,
                'location_id': source,
                # 'product_type': self.product_type,
                'state': 'assigned',
                'move_lines': move_lines,
            })
            self.write({'stock_picking': [(4, stock_picking.id)], 'state': 'done'})

        # """
        #     this ,commented code to open quantities manipulation wizard
        # """
        # lines = []
        # for rec in self.line_ids:
        #     remain = rec.product_qty - self.GetSumOfDonePickgin(rec)
        #     lines.append((0,0,{
        #         'name':rec.name,
        #         'product_id':rec.product_id.id,
        #         'product_qty':rec.product_qty,
        #         'qty_available':rec.qty_available,
        #         'Uom_id':rec.Uom_id.id,
        #         'note':rec.note,
        #         'picking_done':self.GetSumOfDonePickgin(rec),
        #         'picking_quantity':remain,
        #     }))
        # return {
        #     'name': _('Picking Creation'),
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'exchange.wizard',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'target': 'new',
        #     'context':{
        #         'default_exchange_id':self.id,
        #         'default_name':self.name,
        #         'default_Uom_id':rec.Uom_id,
        #         'default_note':rec.note,
        #         'default_line_ids':lines,
        #     }
        # }

    def action_draft(self):
        """
            Move the document to draft state
        """
        self.write({'state': 'draft'})


class ExchangeRequestLine(models.Model):
    _name = 'exchange.request.line'

    exchange_id = fields.Many2one('exchange.request')
    product_id = fields.Many2one('product.product')
    name = fields.Char(required=True, related='product_id.name')
    product_qty = fields.Integer(default=1, string="Ordered Qty")
    Uom_id = fields.Many2one(related='product_id.uom_id')
    note = fields.Char(string="Description")
    qty_available = fields.Float()

    # @api.model
    # def _get_avialable_quantity(self):
    #     """
    #         Return Quantity
    #     """
    #     location = self._context.get('location')
    #     raise ValidationError(location)
    #     quantity = self.env['stock.quant'].search([
    #         ('product_id','=',self.product_id.id),
    #         ('location_id','=',location),
    #     ])
    #     raise ValidationError(quantity)
    #     return quantity.quantity

    @api.constrains('product_qty', 'qty_available')
    def CheckQty(self):
        """
            Chech quantities and make sure that the ordered quantity is
            not more than the available one, and quantity is not zero or less
        """
        for rec in self:
            if rec.product_qty <= 0:
                raise ValidationError(_("Product Quantity Should be greater than zero"))
            # if rec.qty_available <=0 :
            #     raise ValidationError(_("Available Quantity Should be greater than zero"))
            # if rec.product_qty > rec.qty_available:
            #     raise ValidationError(_("You can't Overtake the available Quantity"))


class StockPickingCustom(models.Model):
    _inherit = "stock.picking"

    purchase_order = fields.Many2one('purchase.order')

    def button_validate(self):
        result = super(StockPickingCustom, self).button_validate()
        if self.purchase_order.id:
            self.purchase_order.request_id.exchange_request.write({'state': 'confirm'})
            self.purchase_order.request_id.write({'schedule_date': datetime.now()})
        return result

# class StockPickingTypeCustom(models.Model):
#     _inherit = 'stock.picking.type'

#     @api.constrains('code','warehouse_id','default_location_dest_id','default_location_src_id')
#     def PreventDuplicateLocation(self):
#         if self.code == 'incoming':
#             picktype = self.env['stock.picking.type'].search([
#                 ('code','=','incoming'),
#                 ('warehouse_id','=',self.warehouse_id.id),
#                 ('default_location_dest_id','=',self.default_location_dest_id.id)
#             ])
#             if len(picktype) != 0:
#                 raise ValidationError(_("You can't Duplicate Location"))
#         if self.code == 'outgoing':
#             picktype = self.env['stock.picking.type'].search([
#                 ('code','=','internal'),
#                 ('warehouse_id','=',self.warehouse_id.id),
#                 ('default_location_src_id','=',self.default_location_src_id.id)
#             ])
#             if len(picktype) != 0:
#                 raise ValidationError(_("You can't Duplicate Location"))
