from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    qty_available = fields.Float("Quantity On Hand", store=True, compute="compute_qty_available_warehouse",
                                 digits=dp.get_precision('Product Unit of Measure'), )

    qty_warehouse = fields.Float("Quantity In Warehouse", store=True, compute="compute_qty_available_warehouse",
                                 digits=dp.get_precision('Product Unit of Measure'), )

    @api.depends('product_id')
    def compute_qty_available_warehouse(self):
        for rec in self:
            rec.qty_available = rec.product_id.qty_available
            qty_warehouse = rec.env['stock.quant'].sudo().search(
                [('location_id', '=', rec.order_id.warehouse_id.lot_stock_id.id), ('product_id', '=', rec.product_id.id)])
            rec.qty_warehouse = sum([qty.quantity for qty in qty_warehouse])
