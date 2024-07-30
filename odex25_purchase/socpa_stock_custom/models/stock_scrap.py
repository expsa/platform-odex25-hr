# -*- coding: utf-8 -*-

from odoo import models, fields


class StockScrap(models.Model):
    _inherit = "stock.scrap"

    line_ids = fields.One2many('stock.scrap.line', 'scrap_id')
    committee_members = fields.Many2many('res.users')
    product_id = fields.Many2one('product.product', 'Product', required=False)
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure', required=False)
    state = fields.Selection([
        ('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done')],
        string='Status', default="draft", readonly=True, tracking=True)

    def action_confirm(self):
        self.state = 'confirm'

    def _prepare_move_values(self):
        self.ensure_one()
        move_values = []
        for line in self.line_ids:
            move_values.append({
                'name': self.name,
                'origin': self.origin or self.picking_id.name or self.name,
                'company_id': self.company_id.id,
                'product_id': line.product_id.id,
                'product_uom': line.product_uom_id.id,
                'state': 'draft',
                'product_uom_qty': line.scrap_qty,
                'location_id': self.location_id.id,
                'scrapped': True,
                'location_dest_id': self.scrap_location_id.id,
                'move_line_ids': [(0, 0, {'product_id': line.product_id.id,
                                          'product_uom_id': line.product_uom_id.id,
                                          'qty_done': line.scrap_qty,
                                          'location_id': line.scrap_id.location_id.id,
                                          'location_dest_id': line.scrap_id.scrap_location_id.id,
                                          'package_id': line.package_id.id,
                                          'owner_id': line.scrap_id.owner_id.id,
                                          'lot_id': line.lot_id.id, })]
            })
        return move_values


class StockScrapLine(models.Model):
    _name = "stock.scrap.line"

    scrap_id = fields.Many2one('stock.scrap')
    product_id = fields.Many2one('product.product', domain="[('type', 'in', ['product', 'consu']),"
                                                           " '|', ('company_id', '=', False), "
                                                           "('company_id', '=', company_id)]")
    scrap_qty = fields.Float('Quantity', default=1.0)
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure')
    tracking = fields.Selection(string='Product Tracking', readonly=True, related="product_id.tracking")
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial',
        domain="[('product_id', '=', product_id), ('company_id', '=', company_id)]", check_company=True)
    package_id = fields.Many2one(
        'stock.quant.package', 'Package', check_company=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)
    reason = fields.Text()
