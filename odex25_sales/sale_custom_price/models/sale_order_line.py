from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # @api.model
    # def create(self, vals):
    #     lang = self.env.context.get('lang')
    #     print(lang)
    #     prevent_selling = self.env['ir.config_parameter'].sudo().get_param('sale_custom.prevent_selling')
    #     if prevent_selling:
    #         product_name = self.env['product.product'].browse(vals.get('product_id')).display_name
    #         if vals.get('price_unit') < vals.get('purchase_price'):
    #             raise ValidationError(_("The product '%s' has a sale price less than the cost price.") % product_name)
    #         if vals.get('price_unit') == vals.get('purchase_price'):
    #             raise ValidationError(_("The product '%s' has a sale price equal to the cost price.") % product_name)
    #     return super(SaleOrderLine, self).create(vals)

    @api.model
    def create(self, vals):
        lang = self.env.context.get('lang')
        prevent_selling = self.env['ir.config_parameter'].sudo().get_param('sale_custom_price.prevent_selling')
        if prevent_selling:
            product_id = vals.get('product_id')
            product_name = self.env['product.product'].browse(product_id).display_name

            if vals.get('price_unit') < vals.get('purchase_price'):
                if lang == 'ar_SA':
                    raise ValidationError(_("سعر بيع المنتج '%s' اقل من قيمة التكلفة") % product_name)
                else:
                    raise ValidationError(_("The product '%s' has a sale price less than the cost price.") % product_name)

            elif vals.get('price_unit') == vals.get('purchase_price'):
                if lang == 'ar_SA':
                    raise ValidationError(_("سعر بيع المنتج '%s' مساوي لقيمة التكلفة") % product_name)
                else:
                    raise ValidationError(_("The product '%s' has a sale price equal to the cost price.") % product_name)

        return super(SaleOrderLine, self).create(vals)
