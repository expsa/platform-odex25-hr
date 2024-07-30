from odoo import models, fields, api
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    length = fields.Float(digits='Product Unit of Measure')
    width = fields.Float(digits='Product Unit of Measure')
    product_sold_by_area = fields.Boolean(compute='_compute_product_sold_by_area')

    @api.onchange('length', 'width')
    def _set_product_uom_qty_as_area(self):
        for rec in self:
            if rec.product_sold_by_area:
                rec.product_qty = rec.length * rec.width

    @api.onchange('product_id')
    def _compute_product_sold_by_area(self):
        area_category = self.env.ref('odex25_uom.area_uom_category').id
        for rec in self:
            if rec.product_id:
                rec.product_sold_by_area = (rec.product_id.uom_id.category_id.id == area_category)
            else:
                rec.product_sold_by_area = False