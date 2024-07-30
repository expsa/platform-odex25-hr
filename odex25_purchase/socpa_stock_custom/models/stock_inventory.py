# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_round, float_is_zero


class Inventory(models.Model):
    _name = "stock.inventory"
    _inherit = ['stock.inventory', 'mail.thread', 'mail.activity.mixin']

    state = fields.Selection(selection_add=[('close', 'Rejected'),

                                            ],
                             track_visibility='always')
    state = fields.Selection(string='Status', selection=[
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('cancel', 'Cancelled'),
        ('confirm', 'In Progress'),
        ('first_validate', 'First Validate'),
        ('second_validate', 'Second Validate'),
        ('done', 'Validated')],
                             copy=False, index=True, readonly=True, tracking=True,
                             default='draft')
    reject_reason = fields.Char(string='Reject Reason')
    committee_members = fields.Many2many('res.users')
    committee_head = fields.Many2one('res.users')
    date = fields.Date(string="Start Date")
    sequence = fields.Char('Sequence', default=lambda self: self.env['ir.sequence'].next_by_code(
        'stock.inventory.sequence') or '/')

    @api.onchange('committee_head')
    def on_change_com_head(self):
        if self.committee_head:
            self.committee_members = [self.committee_head.id]
        if not self.committee_head:
            self.committee_members = False

    def action_done(self):
        res = super(Inventory, self).action_done()
        if self.move_ids:
            account_moves = self.env['account.move'].sudo().search([('stock_move_id', 'in', self.move_ids.ids)])
            if account_moves:
                for move in account_moves:
                    move.write({
                        'ref': self.name
                    })
        return res

    def action_confirm(self):
        for rec in self:
            if not rec.committee_head:
                raise ValidationError(_('please select committee head!!'))
            rec.write({
                'state': 'to_approve'
            })

    def action_approve_to_start(self):
        for rec in self:
            rec.state = "pending"

    def action_first_validate(self):
        for rec in self:
            rec.state = "first_validate"

    def action_second_validate(self):
        for rec in self:
            rec.state = "second_validate"

    def action_reject(self):
        if self.env.context['lang'] == 'ar_SY':
            action_name = 'حدد سبب الرفض'
        else:
            action_name = 'Specify Reject Reason'
        return {
            'type': 'ir.actions.act_window',
            'name': action_name,
            'res_model': 'reject.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_origin': self.id, 'default_origin_name': self._name}
        }

    def cancel(self):
        for rec in self:
            rec.write({
                'state': 'close',
                'reject_reason': self.env.context.get('reject_reason')
            })
            rec.message_post(body=_('Inventory Rejected By %s .  With Reject Reason : %s' % (
                str(self.env.user.name), str(rec.env.context.get('reject_reason')))))

    def action_confirm_quant(self):
        self.message_post(body=_('%s Has Signed' % (str(self.env.user.name))))

    def _action_start(self):
        """ Confirms the Inventory Adjustment and generates its inventory lines
        if its state is draft and don't have already inventory lines (can happen
        with demo data or tests).
        """
        for inventory in self:
            if inventory.state != 'pending':
                continue
            vals = {
                'state': 'confirm',
                # 'date': fields.Datetime.now()
            }
            if not inventory.line_ids and not inventory.start_empty:
                self.env['stock.inventory.line'].create(inventory._get_inventory_lines_values())
            inventory.write(vals)

    def action_validate(self):
        if not self.exists():
            return
        self.ensure_one()
        if not self.user_has_groups('stock.group_stock_manager'):
            raise UserError(_("Only a stock manager can validate an inventory adjustment."))
        if self.state != 'second_validate':
            raise UserError(_(
                "You can't validate the inventory '%s', maybe this inventory "
                "has been already validated or isn't ready.", self.name))
        inventory_lines = self.line_ids.filtered(lambda l: l.product_id.tracking in ['lot', 'serial']
                                                 and not l.prod_lot_id and l.theoretical_qty != l.product_qty)
        lines = self.line_ids.filtered(lambda l: float_compare(l.product_qty, 1,
                                                               precision_rounding=l.product_uom_id.rounding) > 0
                                       and l.product_id.tracking == 'serial' and l.prod_lot_id)
        if inventory_lines and not lines:
            wiz_lines = [(0, 0, {'product_id': product.id, 'tracking': product.tracking}) for product in
                         inventory_lines.mapped('product_id')]
            wiz = self.env['stock.track.confirmation'].create({'inventory_id': self.id, 'tracking_line_ids': wiz_lines})
            return {
                'name': _('Tracked Products in Inventory Adjustment'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'views': [(False, 'form')],
                'res_model': 'stock.track.confirmation',
                'target': 'new',
                'res_id': wiz.id,
            }
        self._action_done()
        self.line_ids._check_company()
        self._check_company()
        return True

    def _action_done(self):
        negative = next((line for line in self.mapped('line_ids') if
                         line.product_qty < 0 and line.product_qty != line.theoretical_qty), False)
        if negative:
            raise UserError(_(
                'You cannot set a negative product quantity in an inventory line:\n\t%s - qty: %s',
                negative.product_id.display_name,
                negative.product_qty
            ))
        self.action_check()
        self.write({'state': 'done'})
        self.post_inventory()
        return True


class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    product_default_code = fields.Char(related="product_id.default_code", string="Default Code")
    note = fields.Text()
    increase = fields.Float(compute="_compute_increase_decrease")
    decrease = fields.Float(compute="_compute_increase_decrease")

    @api.depends('difference_qty')
    def _compute_increase_decrease(self):
        for rec in self:
            rec.increase = 0
            rec.decrease = 0
            if rec.difference_qty > 0:
                rec.increase = rec.difference_qty
            if rec.difference_qty < 0:
                rec.decrease = rec.difference_qty
