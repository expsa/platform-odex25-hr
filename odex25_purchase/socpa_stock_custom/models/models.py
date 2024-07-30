# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_round, float_is_zero


class ProductCategory(models.Model):
    _inherit = "product.category"

    property_consignment_account = fields.Many2one('account.account', 'Consigment Account')


class RejectWizard(models.TransientModel):
    _name = 'reject.wizard'

    origin = fields.Integer('')
    reject_reason = fields.Text(string='Reject Reson')
    origin_name = fields.Char('')

    def action_reject(self):
        origin_rec = self.env[self.origin_name].sudo().browse(self.origin)
        if origin_rec:
            origin_rec.write({
                'reject_reason': self.reject_reason
            })
        if dict(origin_rec._fields).get('reject_reason') == None:
            raise ValidationError(_('Sorry This object have no field named Selection Reasoon'))
        else:
            return origin_rec.with_context({'reject_reason': self.reject_reason}).cancel()


class CustomProductTemplate(models.Model):
    _inherit = 'product.template'

    allowed_jobs = fields.Many2many(comodel_name='hr.job', string='Allowed Jobs')
    git_product = fields.Boolean('Can Be Gift')
    available_for = fields.Selection(string='Available For', track_visibility='always',
                                     selection=[('department', 'Department'), ('job', 'Job'), ('employee', 'Employee')])
    gift_quants = fields.One2many(comodel_name='gift.product.quant', inverse_name='product_id', string='Gift Quants')

    @api.onchange('available_for')
    def available_for_change(self):
        for line in self.gift_quants:
            line.emloyee_id = False
            line.department_id = False
            line.job_id = False


class StockLocationCustom(models.Model):
    _inherit = 'stock.location'

    user_ids = fields.Many2many(comodel_name='res.users', string='Resposible')
    is_supply = fields.Boolean(string='Is Supply Location')

    def name_get(self):
        get_all = self.env.context.get('get_all', False)
        requisition_type = self.env.context.get('requisition_type', False)
        employees = None
        result = []
        if get_all and requisition_type == 'stock_transfer':
            locations = self.env['stock.location'].sudo().search([('active', '=', True), ('is_supply', '=', True)])
            result = [(location.id, location.name) for location in locations]
            return result
        else:
            return super(StockLocationCustom, self).name_get()


class StockWarehouseCustom(models.Model):
    _inherit = 'stock.picking.type'

    user_ids = fields.Many2many(comodel_name='res.users', string='Resposible')


class GiftProducts(models.Model):
    _name = 'gift.product.quant'
    _description = 'New Description'

    product_id = fields.Many2one(comodel_name='product.template', string='Product')
    department_id = fields.Many2one(comodel_name='hr.department', string='Department')
    job_id = fields.Many2one(comodel_name='hr.job', string='Job')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    planned_qty = fields.Integer(string='Planned Qty', track_visibility='always')
    actual_qty = fields.Integer(string='Actual Qty')
    remain_qty = fields.Integer(string='Remain Qty', compute="_compute_remain_qty", store=True)

    @api.depends('planned_qty', 'actual_qty')
    def _compute_remain_qty(self):
        for rec in self:
            rec.remain_qty = rec.planned_qty - rec.actual_qty

    @api.model
    def write(self, values):
        for rec in self:
            if 'planned_qty' in values:
                rec.product_id.message_post(_("planned amount of product %s changed from %s to %s" % (
                    self.product_id.name, rec.planned_qty, values['planned_qty'])))
            return super(GiftProducts, self).write(values)

    @api.constrains('employee_id')
    def onchange_employee(self):
        for rec in self:
            if rec.product_id.available_for == 'employee' and rec.product_id.gift_quants.filtered(
                    lambda quant: quant.employee_id.id == rec.employee_id.id and quant.id != rec.id):
                raise ValidationError(_("you cannot duplicate employee"))

    @api.constrains('job_id')
    def onchange_job(self):
        for rec in self:
            if rec.product_id.available_for == 'job' and rec.job_id and rec.product_id.gift_quants.filtered(
                    lambda quant: quant.job_id and quant.job_id.id == rec.job_id.id and quant.id != rec.id):
                raise ValidationError(_("you cannot duplicate job"))

    @api.constrains('department_id')
    def onchange_department(self):
        for rec in self:
            if rec.product_id.available_for == 'department' and rec.product_id.gift_quants.filtered(
                    lambda quant: quant.department_id.id == rec.department_id.id and quant.id != rec.id):
                raise ValidationError(_("you cannot duplicate department"))


class StockPickingCustom(models.Model):
    _inherit = 'stock.picking'

    is_consigment = fields.Boolean(string='Consigment Goods?')

    def _action_done(self):
        super_action = super(StockPickingCustom, self)._action_done()
        exchane_request = self.env['exchange.request'].search([('recieve_picking_id', '=', self.id)])
        if exchane_request:
            exchane_request.write({
                'state': 'done'
            })
        else:
            self.env.cr.execute("""
                select exchange_request_id from exchange_request_stock_picking_rel where stock_picking_id = """ +str(
                self.id) + """;
            """)
            excange_request_id = self.env.cr.fetchall()
            if len(excange_request_id) > 0:
                exchane_request = self.env['exchange.request'].browse(excange_request_id[0])
                if not exchane_request.sudo().recieve_picking_id:
                    exchane_request.write({
                        'state': 'done'
                    })
                else:
                    exchane_request.sudo().write({
                        'state': 'on_the_way'
                    })
        return super_action

    def action_cancel(self):
        super_action = super(StockPickingCustom, self).action_cancel()
        exchane_request = None
        if self.id:
            self.env.cr.execute("""
                select exchange_request_id from exchange_request_stock_picking_rel where stock_picking_id = """ + str(
                self.id) + """;
            """)
        excange_request_id = self.env.cr.fetchall()
        if len(excange_request_id) > 0:
            exchane_request = self.env['exchange.request'].browse(excange_request_id[0])
            exchane_request.write({
                'state': 'cancel'
            })
        return super_action


class StockMoveCustom(models.Model):
    _inherit = 'stock.move'

    """ 
        override acountig entries to make move to Consigment account instaid of expense account
    """

    def _account_entry_move(self, qty, description, svl_id, cost):
        """ Accounting Valuation Entries """
        self.ensure_one()
        location_from = self.location_id
        location_to = self.location_dest_id
        company_from = self._is_out() and self.mapped('move_line_ids.location_id.company_id') or False
        company_to = self._is_in() and self.mapped('move_line_ids.location_dest_id.company_id') or False
        if not self.picking_id.is_consigment:
            return super(StockMoveCustom, self)._account_entry_move(qty, description, svl_id, cost)
        else:
            consigment_account = self.product_id.categ_id.property_consignment_account
            if not consigment_account:
                raise ValidationError(
                    _('This product %s has no Consigment Account Please Set it in Product Category and try again' % (
                        self.product_id.name)))
            else:
                journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
                if location_from and location_from.usage == 'customer':  # goods returned from customer
                    self._create_account_move_line(consigment_account.id, acc_valuation, journal_id, qty, description,
                                                   svl_id, cost)
                else:
                    self._create_account_move_line(acc_valuation, consigment_account.id, journal_id, qty, description,
                                                   svl_id, cost)

    """
        Override Done method to read locations to bypass the record rule with the operations
    
    """
    # def _action_done(self):
    #     self.filtered(lambda move: move.state == 'draft')._action_confirm()  # MRP allows scrapping draft moves
    #     moves = self.exists().filtered(lambda x: x.state not in ('done', 'cancel'))
    #     moves_todo = self.env['stock.move']

    #     # Cancel moves where necessary ; we should do it before creating the extra moves because
    #     # this operation could trigger a merge of moves.
    #     for move in moves:
    #         if move.quantity_done <= 0:
    #             if float_compare(move.product_uom_qty, 0.0, precision_rounding=move.product_uom.rounding) == 0:
    #                 move._action_cancel()

    #     # Create extra moves where necessary
    #     for move in moves:
    #         if move.state == 'cancel' or move.quantity_done <= 0:
    #             continue
    #         # extra move will not be merged in mrp
    #         if not move.picking_id:
    #             moves_todo |= move
    #         moves_todo |= move._create_extra_move()

    #     # Split moves where necessary and move quants
    #     for move in moves_todo:
    #         # To know whether we need to create a backorder or not, round to the general product's
    #         # decimal precision and not the product's UOM.
    #         rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')
    #         if float_compare(move.quantity_done, move.product_uom_qty, precision_digits=rounding) < 0:
    #             # Need to do some kind of conversion here
    #             qty_split = move.product_uom._compute_quantity(move.product_uom_qty - move.quantity_done, move.product_id.uom_id, rounding_method='HALF-UP')
    #             new_move = move._split(qty_split)
    #             for move_line in move.move_line_ids:
    #                 if move_line.product_qty and move_line.qty_done:
    #                     # FIXME: there will be an issue if the move was partially available
    #                     # By decreasing `product_qty`, we free the reservation.
    #                     # FIXME: if qty_done > product_qty, this could raise if nothing is in stock
    #                     try:
    #                         move_line.write({'product_uom_qty': move_line.qty_done})
    #                     except UserError:
    #                         pass
    #             move._unreserve_initial_demand(new_move)
    #         move.move_line_ids._action_done()
    #     # Check the consistency of the result packages; there should be an unique location across
    #     # the contained quants.
    #     for result_package in moves_todo\
    #             .mapped('move_line_ids.result_package_id')\
    #             .filtered(lambda p: p.quant_ids and len(p.quant_ids) > 1):
    #         if len(result_package.quant_ids.mapped('location_id')) > 1:
    #             raise UserError(_('You should not put the contents of a package in different locations.'))
    #     picking = moves_todo and moves_todo[0].picking_id or False
    #     moves_todo.write({'state': 'done', 'date': fields.Datetime.now()})
    #     moves_todo.mapped('move_dest_ids').sudo()._action_assign()


class StockScrapCustom(models.Model):
    _inherit = 'stock.scrap'

    def _get_default_scrap_location_id(self):
        scrap = self.env['stock.location'].search([('scrap_location', '=', True), ('user_ids', 'in', self.env.user.id),
                                                   ('company_id', 'in', [self.env.user.company_id.id, False])],
                                                  limit=1).id
        if scrap:
            return scrap.id
        return None

    def _get_default_location_id(self):
        user_location = self.env['stock.location'].search([('user_ids', 'in', self.env.user.id)], limit=1)
        print("warehouse---------------", user_location)
        if user_location:
            return user_location.id
        else:
            raise UserError(_('You must responsible in at least one location '))

    location_id = fields.Many2one(
        'stock.location', 'Location', domain="[('usage', '=', 'internal')]",
        required=True, states={'done': [('readonly', True)]}, default=_get_default_location_id)
    scrap_location_id = fields.Many2one(
        'stock.location', 'Scrap Location', default=_get_default_scrap_location_id,
        domain="[('scrap_location', '=', True)]", required=True, states={'done': [('readonly', True)]})
    scrapping_reason = fields.Text(string='Scrapping Reason')
