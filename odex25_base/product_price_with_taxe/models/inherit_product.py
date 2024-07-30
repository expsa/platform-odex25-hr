from odoo import api, fields, models


class ProductInherit(models.Model):
    _inherit = 'product.template'

    price_with_taxe = fields.Float(string="Price with Tax", required=False, compute="_compute_price_with_taxe", store=True)

    @api.depends('list_price', 'taxes_id')
    def _compute_price_with_taxe(self):
        for rec in self:
            taxe = rec.taxes_id[0] if rec.taxes_id else False
            amount_tax = 0
            if taxe:
                amount = taxe.compute_all(rec.list_price,
                                          currency=rec.currency_id,
                                          quantity=1,
                                          product=None,
                                          partner=None)['taxes'][0]
                amount_tax = amount['amount']
            rec.price_with_taxe = rec.list_price + amount_tax


class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    price_with_taxe = fields.Float(related="product_tmpl_id.price_with_taxe", required=False, )
