from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    show_qty_available = fields.Boolean(help="Show Product Qtys in POS", default=True)
    stock_location_id = fields.Many2one(related='picking_type_id.default_location_src_id')
    hide_out_of_stock_products = fields.Boolean()
    min_reserve_qty = fields.Integer(string='Deny order when quantity available lower than')
    allow_out_of_stock = fields.Boolean(string='Allow Out-of-Stock')


