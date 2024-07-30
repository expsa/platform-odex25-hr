from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def check_qty_before_add(self):
        for rec in self:
            if (rec.product_id.type == 'product') and (not rec.product_id.allow_negative_stock):
                if rec.qty_available > 0 or rec.qty_warehouse > 0:
                    rec.product_uom_qty = 1
                else:
                    rec.product_uom_qty = 0
            else:
                rec.product_uom_qty = 1

    @api.onchange('product_uom_qty')
    def check_qty_for_selected_product(self):
        for rec in self:
            if (rec.product_id.type == 'product') and (not rec.product_id.allow_negative_stock):
                if rec.product_uom_qty > rec.qty_available and rec.product_uom_qty != 0:
                    rec.product_uom_qty = rec.qty_available if rec.qty_available > 0 else 0

                    warning_mess = {
                        'message': _("You can not sell more than you have in all warehouse.")
                    }
                    return {'warning': warning_mess}
                    raise UserError()

    # @api.onchange('product_uom_qty', 'product_uom', 'route_id')
    # def _onchange_product_id_check_availability(self):
    #     if not self.product_id or not self.product_uom_qty or not self.product_uom:
    #         self.product_packaging = False
    #         return {}
    #     if self.product_id.type == 'product':
    #         precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
    #         product = self.product_id.with_context(
    #             warehouse=self.order_id.warehouse_id.id,
    #             lang=self.order_id.partner_id.lang or self.env.user.lang or 'en_US'
    #         )
    #         product_qty = self.product_uom._compute_quantity(self.product_uom_qty, self.product_id.uom_id)
    #         if float_compare(product.virtual_available, product_qty, precision_digits=precision) == -1:
    #             is_available = self._check_routing()
    #             if not is_available:
    #                 if not self.product_id.allow_negative_stock:
    #                     raise UserError(_("You can not sell this product in negative."))
    #                 message = _('You plan to sell %s %s but you only have %s %s available in %s warehouse.') % \
    #                           (self.product_uom_qty, self.product_uom.name, product.virtual_available,
    #                            product.uom_id.name, self.order_id.warehouse_id.name)
    #                 # We check if some products are available in other warehouses.
    #                 if float_compare(product.virtual_available, self.product_id.virtual_available,
    #                                  precision_digits=precision) == -1:
    #                     message += _('\nThere are %s %s available accross all warehouses.') % \
    #                                (self.product_id.virtual_available, product.uom_id.name)
    #                 warning_mess = {
    #                     'title': _('Not enough inventory!'),
    #                     'message': message
    #                 }
    #                 return {'warning': warning_mess}
    #     return {}

    # @api.onchange('product_uom_qty', 'product_uom', 'route_id')
    # def _onchange_product_id_check_availability(self):
    #     if not self.product_id or not self.product_uom_qty or not self.product_uom:
    #         self.product_packaging = False
    #         return {}
    #     if self.product_id.type == 'product':
    #         precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
    #         product = self.product_id.with_context(
    #             warehouse=self.order_id.warehouse_id.id,
    #             lang=self.order_id.partner_id.lang or self.env.user.lang or 'en_US'
    #         )
    #         product_qty = self.product_uom._compute_quantity(self.product_uom_qty, self.product_id.uom_id)
    #         if float_compare(product.virtual_available, product_qty, precision_digits=precision) == -1:
    #             is_available = self._check_routing()
    #             if not is_available:
    #                 message = _('You plan to sell %s %s but you only have %s %s available in %s warehouse.') % \
    #                           (self.product_uom_qty, self.product_uom.name, product.virtual_available,
    #                            product.uom_id.name, self.order_id.warehouse_id.name)
    #                 # We check if some products are available in other warehouses.
    #                 if float_compare(product.virtual_available, self.product_id.virtual_available,
    #                                  precision_digits=precision) == -1:
    #                     message += _('\nThere are %s %s available accross all warehouses.') % \
    #                                (self.product_id.virtual_available, product.uom_id.name)
    #                     if self.product_id.virtual_available <= 0 and not self.product_id.allow_negative_stock:
    #                         raise UserError(_("You can not sell this product in negative." + message))
    #                 warning_mess = {
    #                     'title': _('Not enough inventory!'),
    #                     'message': message
    #                 }
    #                 return {'warning': warning_mess}
    #     return {}