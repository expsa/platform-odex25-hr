
import logging

from odoo import _, api, fields, models
from odoo.tools import float_is_zero
from odoo.exceptions import *

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"

    returned_order = fields.Boolean("Returned Order", default=False)
    
    @api.model
    def create_from_ui(self, orders, draft=False):
        # Keep return orders
        for order in orders:
            if 'server_id' in order['data']:
                existing_order = self.env['pos.order'].search(['|', ('id', '=', order['data']['server_id']), ('pos_reference', '=', order['data']['name'])], limit=1)
            if (existing_order and order.get('data', {}).get('mode') == 'return'):
                existing_order.with_context(return_lines=order.get('data', {}).get('lines'), return_from_ui=True).refund()
        return super(PosOrder, self).create_from_ui(orders, draft)
    
    def refund(self):
        if self._context.get('return_from_ui'):        
            _logger.info('Overriding refund method of model pos.order without calling super.')
            for order in self:
                current_session = order.session_id.config_id.current_session_id
                order_refund_data = order._prepare_refund_values(current_session)
                order_refund_data.update({'returned_order': True})
                refund_order = order.copy(order_refund_data)
                return_lines = self._context.get('return_lines')
                if return_lines:
                    return_lines = [line[2] for line in return_lines]
                    for line in order.lines:
                        return_line = list(filter(lambda rec: rec.get('product_id') == line.product_id.id, return_lines))
                        if not return_line:
                            continue
                        return_line = return_line[0]
                        qty_data = {k: v for k, v in return_line.items() if k in ('qty', 'price_subtotal', 'price_subtotal_incl')}
                        PosOrderLineLot = self.env['pos.pack.operation.lot']
                        for pack_lot in line.pack_lot_ids:
                            PosOrderLineLot += pack_lot.copy()
                        refund_data = line._prepare_refund_data(refund_order, PosOrderLineLot)
                        refund_data.update(qty_data)
                        line.copy(refund_data)
                    refund_order._compute_batch_amount_all()
                    refund_order.make_payment()
        else:
            return super().refund()
                
    def make_payment(self):
        self.ensure_one()
        currency = self.currency_id
        amount = self.amount_total - self.amount_paid
        if not float_is_zero(amount, precision_rounding=currency.rounding):
            self.add_payment({
                'pos_order_id': self.id,
                'amount': self._get_rounded_amount(amount),
                'payment_method_id': self.session_id.payment_method_ids.sorted(lambda pm: pm.is_cash_count, reverse=True)[:1].id,
            })

        if self._is_pos_order_paid():
            self.action_pos_order_paid()
            self._create_order_picking()