# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

import logging
import requests

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare

_logger = logging.getLogger(__name__)


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    # provider = fields.Selection(selection_add=[('telr', 'Telr')])
    provider = fields.Selection(selection_add=[
        ('telr', "Telr"),
    ], ondelete={'telr': 'set default'})
    telr_merchant_id = fields.Char(string='Merchant ID')
    telr_api_key = fields.Char('API Key')
    web_url = fields.Char('Web Url')

    # @api.multi
    def telr_form_generate_values(self, values):
        self.ensure_one()
        # base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url = self.web_url
        telr_tx_values = {}
        telr_tx_values.update({
            "tx_url": '/payment/telr/prepay',
            'base_url': base_url,
            'reference': values['reference'],
            'amount': values['amount'],
            'currency': values['currency'],
        })
        return telr_tx_values

    #     @api.multi
    def telr_get_form_action_url(self):
        self.ensure_one()
        # base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url = self.web_url
        return base_url + '/payment/telr/prepay'


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    telr_order_id = fields.Char(string='Telr Order ID')

    def _get_telr_tx_status(self, telr_order_id):
        url = "https://secure.telr.com/gateway/order.json"
        payload = {
            "ivp_method": "check",
            "ivp_store": int(self.acquirer_id.telr_merchant_id),
            "ivp_authkey": self.acquirer_id.telr_api_key,
            "order_ref": telr_order_id,
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        res = requests.request("POST", url, data=payload, headers=headers)
        response = res.json()
        return response

    @api.model
    def _telr_form_get_tx_from_data(self, data):
        reference = data.get('cartid')
        if not reference:
            error_msg = _(
                'Telr: Received data with missing reference %s') % reference
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        txs = self.env['payment.transaction'].search([('reference', '=', reference), ('provider', '=', 'telr')])
        if not txs or len(txs) > 1:
            error_msg = 'Telr: received data for reference %s' % (reference)
            if not txs:
                error_msg += '; No order found'
            else:
                error_msg += '; Multiple order found'
            _logger.info(error_msg)
            raise ValidationError(error_msg)
        return txs[0]

    #     @api.multi
    def _telr_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        order_data = data.get('order')
        txn_id = order_data and order_data.get('ref')

        if self.acquirer_reference and txn_id != self.acquirer_reference:
            invalid_parameters.append(('Order Id', txn_id, self.acquirer_reference))

        if float_compare(float(order_data.get('amount', '0.0')), self.amount, 2) != 0:
            invalid_parameters.append(('Amount', order_data.get('amount'), '%.2f' % self.amount))
        return invalid_parameters

    def _telr_form_validate(self, data):
        ORDER_STATUS_PAID = 3
        ORDER_STATUS_AUTHORISED = 2
        ORDER_STATUS_PENDING = 1
        ORDER_STATUS_CANCELLED = -2

        order_data = data.get('order')
        status = order_data.get('status')
        tx_ref = order_data and order_data.get('ref')
        tx_msg = order_data and order_data.get('message')

        if status.get('code') == ORDER_STATUS_PAID:
            self.write({
                'state': 'done',
                'acquirer_reference': tx_ref
            })
            # self._set_transaction_done()
            return True
        elif status.get('code') == ORDER_STATUS_PENDING:
            self.write({
                'state': 'pending',
                'acquirer_reference': tx_ref,
                'state_message': tx_msg
            })
            return True
        elif status.get('code') == ORDER_STATUS_AUTHORISED:
            self.write({
                'state': 'authorized',
                'acquirer_reference': tx_ref,
                'state_message': tx_msg
            })
            return True
        elif status.get('code') == ORDER_STATUS_CANCELLED:
            self.write({
                'state': 'cancel',
                'acquirer_reference': tx_ref,
                'state_message': tx_msg
            })
            return True
        else:
            _logger.info(status.get('text'))
            self.write({
                'state': 'error',
                'state_message': status.get('text'),
                'acquirer_reference': tx_ref,
            })
            return False
