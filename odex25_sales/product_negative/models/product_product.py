from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    allow_negative_stock = fields.Boolean(
        string='Allow Negative Stock',
        default=True,
        help="If this option is not active on this product nor on its "
             "product category and that this product is a stockable product, "
             "then the validation of the related stock moves will be blocked if "
             "the stock level becomes negative with the stock move.")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    allow_negative_stock = fields.Boolean(related='product_tmpl_id.allow_negative_stock', )
