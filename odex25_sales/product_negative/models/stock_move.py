from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.onchange('quantity_done')
    def check_qty_before_add(self):
        for rec in self:
            if not rec.product_id.allow_negative_stock and rec.picking_id.picking_type_id.code == 'outgoing':
                if rec.quantity_done > rec.product_id.qty_available:
                    raise UserError(_(f"You can not deliver more than you have in stock {rec.product_id.qty_available}, "
                                      "please allow stock negative for this product."))