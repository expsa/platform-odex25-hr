from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    post_move_location_qty = fields.Float("Qty after move", digits='Product Unit of Measure')

    def set_qty_warehouse(self):
        quant_obj = self.env['stock.quant']
        for rec in self:
            location_qty = sum(quant_obj.sudo().search([('location_id', '=', rec.location_id.id),
                                                    ('product_id', '=', rec.product_id.id)])\
                                                    .mapped('quantity'))
            rec.write({'post_move_location_qty': location_qty - rec.qty_done})

    def _action_done(self):
        self.set_qty_warehouse()    
        return super(StockMoveLine, self)._action_done()