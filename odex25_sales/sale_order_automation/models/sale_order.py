from odoo import api, fields, models, exceptions


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm()
        for order in self:

            warehouse = order.warehouse_id
            if warehouse.is_delivery_set_to_done and order.picking_ids: 
                for picking in self.picking_ids:
                    picking.action_confirm()
                    picking.action_assign()
                    if picking.state == 'assigned':
                        for move in picking.move_lines.filtered(lambda m: m.state not in ['done', 'cancel']):
                            for move_line in move.move_line_ids:
                                move_line.qty_done = move_line.product_uom_qty
                        picking.with_context(skip_immediate=True).button_validate()
            self._cr.commit()

            if warehouse.create_invoice and not order.invoice_ids:
                order._create_invoices()  

            if warehouse.validate_invoice and order.invoice_ids:
                for invoice in order.invoice_ids:
                    invoice.action_post()
            
        return res  
