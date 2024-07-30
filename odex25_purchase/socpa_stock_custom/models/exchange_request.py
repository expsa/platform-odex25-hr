# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ExchangeRequestCustom(models.Model):
    _inherit = "exchange.request"

    type = fields.Selection(selection_add=[('gift', 'Gift')])
    requisition_type = fields.Selection(selection_add=[('stock_transfer', 'Stock Transfer')])
    dest_location_id = fields.Many2one('stock.location', 'Destination ')
    recieve_picking_id = fields.Many2one('stock.picking', 'Receive Operation',
                                         help="the Recive operation is the operation in destination location in case "
                                              "of internal transfer")
    state = fields.Selection(selection_add=[('on_the_way', 'On The Way')])
    product_type = fields.Selection(selection=[('material', 'Material'), ('service', 'Service')], default='material')

    @api.onchange('warehouse_id')
    def GetPickingType(self):
        """
            Set Default Value For picking type
        """
        picktype = False
        location = False
        if self.warehouse_id:
            if self.requisition_type == 'stock_transfer':
                picktype = self.env['stock.picking.type'].sudo().search([
                    ('code', '=', 'internal'),
                    ('warehouse_id', '=', self.warehouse_id.id)
                ])
                if not picktype:
                    raise ValidationError(_('Please Create Operation of type internal Transfer for this warehouse'))
                self.picking_type_id = picktype and picktype[0].id
            else:
                return super(ExchangeRequestCustom, self).GetPickingType()

    def action_confirm(self):
        """
            Move docuemtn to confirm state
        """
        move_lines = []
        if len(self.line_ids) == 0:
            raise ValidationError(_("Please add products before confirming your order"))
        if self.requisition_type == 'stock_transfer':
            for rec in self.line_ids:
                move_lines.append((0, 0, {
                    'name': self.name,
                    'product_id': rec.product_id.id,
                    'product_uom_qty': rec.product_qty,
                    'product_uom': rec.Uom_id.id,
                    'location_dest_id': self.dest_location_id.id,
                }))
            if len(move_lines) != 0:
                stock_picking = self.env['stock.picking'].sudo().create({
                    'date': self.request_date,
                    'partner_id': self.user_id.partner_id.id,
                    'origin': self.name,
                    'picking_type_id': self.picking_type_id.sudo().id,
                    'location_dest_id': self.dest_location_id.id,
                    'location_id': self.location_id.id,
                    'state': 'assigned',
                    'note': self.purpose,
                    'move_lines': move_lines,
                })
            self.write({
                'state': 'to_deliver',
                'stock_picking': [(4, stock_picking.id)]
            })
            stock_picking.message_post(body=_('This Picking is created from supply request No %s' % (str(self.name))))
            if stock_picking.move_lines and stock_picking.move_lines[0].move_dest_ids:
                self.recieve_picking_id = stock_picking.move_lines[0].move_dest_ids[0].picking_id.id

        else:
            self.write({'state': 'confirm'})

    def action_exchange_wizard(self):
        super_action = super(ExchangeRequestCustom, self).action_done()
        if self.stock_picking:
            for line in self.stock_picking.move_lines:
                quant_line = line.product_id.gift_quants.filtered(lambda l:
                                                                  l.employee_id.id == self.employee_id.id or
                                                                  (
                                                                              l.department_id.id == self.employee_id.department_id.id or
                                                                              l.job_id.id == self.employee_id.job_id.id)
                                                                  )
                if quant_line:
                    quant_line.write({
                        'actual_qty': quant_line[0].actual_qty + line.product_uom_qty
                    })
        return super_action


class ExchangeRequestLineCustom(models.Model):
    _inherit = 'exchange.request.line'

    @api.onchange('product_qty')
    def validate_product_qty(self):
        for rec in self:
            if rec.exchange_id.type == 'gift':
                quant_line = rec.product_id.gift_quants.filtered(lambda l:
                                                                 l.employee_id.id == rec.exchange_id.employee_id.id or
                                                                 (
                                                                             l.department_id.id == rec.exchange_id.employee_id.department_id.id or
                                                                             l.job_id.id == rec.exchange_id.employee_id.job_id.id)
                                                                 )
                if quant_line and rec.product_qty > quant_line.remain_qty:
                    raise ValidationError(
                        _("You Have Exceded The Max gift allowed  Quantity For this Product: %s .\n\n The Available quant is %s" % (
                        rec.product_id.name, quant_line.remain_qty)))
