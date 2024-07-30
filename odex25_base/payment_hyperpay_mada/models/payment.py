# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

import json
import re
import logging
from odoo.exceptions import UserError

from urllib.parse import urljoin
from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
import requests

_logger = logging.getLogger(__name__)


class AcquirerMADA(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('hyperpay_mada', 'HyperPay MADA')], ondelete={'hyperpay_mada': 'set default'})
    hyperpay_mada_entity_id = fields.Char(string='Merchant ID/Entity Id', required_if_provider='hyperpay_mada',
                                     groups='base.group_user')
    hyperpay_mada_authorization_bearer = fields.Char(
        string='Authorization Bearer', required_if_provider='hyperpay_mada', groups='base.group_user')

    @api.model
    def _get_authorize_urls_hyperpay_mada(self, environment):
        """ hyperpay_mada URLS """

        if environment == 'prod':
            return {
                'hyperpay_mada_form_url': 'https://oppwa.com/v1/checkouts',

            }
        else:
            return {
                'hyperpay_mada_form_url': 'https://oppwa.com/v1/checkouts',
            }

    def _get_authenticate_hyperpay_mada(self, values):
        url = "https://oppwa.com/v1/checkouts" if self.state == 'test' else "https://oppwa.com/v1/checkouts"
        authorization_bearer = "Bearer " + self.hyperpay_mada_authorization_bearer
        print("<<", authorization_bearer)
        data = {
            'entityId': self.hyperpay_mada_entity_id,
            # 'testMode': 'EXTERNAL',
            'amount': str(format(values['amount'], '.2f')),
            'currency': values['currency'] and values['currency'].name or '',
            'paymentType': 'DB',
            'merchantTransactionId': values.get('reference'),
            'customer.email': values['partner_email'],
            'customer.givenName': values['partner_name'],
            'customer.companyName': values['billing_partner_commercial_company_name'],
            'customer.phone': values['partner_phone'],
            'billing.street1': values['billing_partner_address'],
            'billing.city': values['billing_partner_city'],
            'billing.state': values['billing_partner_state'].name,
            'billing.country': values['billing_partner_country'].code,
            'billing.postcode': values['billing_partner_zip'],
            'customer.surname': values['partner_last_name']

        }
        try:
            headers = {'Authorization': authorization_bearer}
            response = requests.post(
                url,
                headers=headers,
                data=data
            )
            response = json.loads(response.text)
            print("RESPONSE................", response)
            return response.get('id')
        except Exception as e:
            raise UserError(_(e))

    def hyperpay_mada_form_generate_values(self, values):
        # if 'partner_id' in values:
        partner = self.env['res.partner'].browse(values['partner_id'])
        base_url = self.get_base_url()
        check_out_id = self._get_authenticate_hyperpay_mada(values)
        print(">>", self.hyperpay_mada_authorization_bearer)
        authorization_bearer = "Bearer " + self.hyperpay_mada_authorization_bearer
        hyperpay_mada_tx_values = dict(values)
        hyperpay_mada_tx_values.update({
            'entityId': self.hyperpay_mada_entity_id,
            'check_out_id': check_out_id,
            'Authorization': authorization_bearer,
            'amount': str(format(values['amount'], '.2f')),
            'currency': values['currency'] and values['currency'].name or '',
            'paymentBrand': 'VISA',
            'paymentType': 'DB',
            'merchantTransactionId': values.get('reference'),
            'shopperResultUrl': '%s' % urljoin(base_url, '/shop/hyperpay_mada/payment/'),
            'hyperpay_return': '%s' % urljoin(base_url, '/payment/hyperpay_mada/return'),
            'custom': json.dumps({'return_url': '%s' % hyperpay_mada_tx_values.pop('return_url')}) if hyperpay_mada_tx_values.get(
                'return_url') else False,
        })
        return hyperpay_mada_tx_values

    def hyperpay_mada_get_form_action_url(self):
        self.ensure_one()
        environment = 'prod' if self.state == 'enabled' else 'test'
        return self._get_authorize_urls_hyperpay_mada(environment)['hyperpay_mada_form_url']


class Txhyperpay_mada(models.Model):
    _inherit = 'payment.transaction'

    # --------------------------------------------------
    # FORM RELATED METHODS
    # --------------------------------------------------

    @api.model
    def _hyperpay_mada_form_get_tx_from_data(self, data):
        print("DATA.................", data)
        _logger.info(data)
        reference, txn_id = data.get('merchantTransactionId'), data.get('id')

        if not reference or not txn_id:
            error_msg = _('hyperpay_mada: received data with missing reference (%s) or (%s)') % (reference, txn_id)
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        # find tx -> @TDENOTE use txn_id ?
        txs = self.env['payment.transaction'].search([('reference', '=', reference)])
        if not txs or len(txs) > 1:
            error_msg = 'hyperpay_mada: received data for reference %s' % (reference)
            if not txs:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.info(error_msg)
            raise ValidationError(error_msg)
        return txs[0]

    def _hyperpay_mada_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        if self.acquirer_reference and data.get('id') != self.acquirer_reference:
            invalid_parameters.append(('id', data.get('id'), self.acquirer_reference))
        return invalid_parameters

    def _hyperpay_mada_form_validate(self, data):
        status_code = data.get('result').get('code')
        success_regex_1 = re.compile(r'000\.000\.|000\.100\.1|000\.[36]').search(status_code)
        success_regex_2 = re.compile(r'000\.400\.0[^3]|000\.400\.100').search(status_code)
        pending_regex_1 = re.compile(r'000\.200').search(status_code)
        pending_regex_2 = re.compile(r'800\.400\.5|100\.400\.500').search(status_code)
        error_regex_1 = re.compile(r'000\.100\.2').search(status_code)
        if success_regex_1 or success_regex_2:
            success_message = data.get('result').get('description') or 'success'
            logger_msg = _('hyperpay_mada:' + success_message)
            _logger.info(logger_msg)
            self.write({
                'acquirer_reference': data.get('id'),
            })
            self._set_transaction_done()
            return True
        elif pending_regex_1 or pending_regex_2:
            pending_message = data.get('result').get('description') or 'pending'
            logger_msg = _('hyperpay_mada:' + pending_message)
            _logger.info(logger_msg)
            self.write({'acquirer_reference': data.get('id')})
            self._set_transaction_pending()
            return True
        elif error_regex_1:
            error_message = data.get('result').get('description') or 'error'
            error = _('hyperpay_mada:' + error_message)
            _logger.info(error)
            self.write({'state_message': error})
            self._set_transaction_cancel()
            return False
        else:
            cancel_message = data.get('result').get('description') or 'cancel'
            logger_msg = _('hyperpay_mada:' + cancel_message)
            _logger.info(logger_msg)
            self.write({'acquirer_reference': data.get('id')})
            self._set_transaction_cancel()
            return True
