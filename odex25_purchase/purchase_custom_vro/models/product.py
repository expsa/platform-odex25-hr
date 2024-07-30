# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_ok = fields.Boolean('Can be Sold', default=False)

    stock_ok = fields.Boolean('Can be Stock', default=False)


class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_valuation = fields.Selection([
        ('manual_periodic', 'Manual'),
        ('real_time', 'Automated')], default="manual_periodic", string='Inventory Valuation',
        company_dependent=True, copy=True, required=True,
        help="""Manual: The accounting entries to value the inventory are not posted automatically.
        Automated: An accounting entry is automatically created to value the inventory when a product enters or
         leaves the company.""")
    # service_id = fields.Many2one(comodel_name='product.product',
    #                              string='Service',
    #                              domain=[('type', '=', 'service'), ('initiative_id', '!=', False)])
