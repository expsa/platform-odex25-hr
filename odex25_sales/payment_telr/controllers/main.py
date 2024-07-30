# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

import json
import logging
import pprint
import requests
import werkzeug
from werkzeug import urls

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
_logger = logging.getLogger(__name__)


class TelrController(http.Controller):
    _return_url = '/payment/telr/return'

    @http.route('/payment/telr/prepay', type='http', auth="none", methods=['POST'], csrf=False)
    def telr_prepay(self, **post):
        # base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        TX = request.env['payment.transaction'].sudo().search([
            ('reference', '=', post.get('reference'))], limit=1)
        acquirer = TX.acquirer_id
        base_url = acquirer.web_url
        url = "https://secure.telr.com/gateway/order.json"
        sequence = request.env["ir.sequence"].sudo().next_by_code("payment.transaction")
        partner_id = TX.partner_id
        _logger.info('partner_id partner_id %s', partner_id)
        _logger.info('country_id country_id %s', partner_id.country_id.name)
        # _logger.info('request.env.user %s', request.env.user)

        payload = {
            "ivp_method": "create",
            # "ivp_store": int(acquirer.telr_merchant_id),
            "ivp_store": acquirer.telr_merchant_id,
            "ivp_authkey": acquirer.telr_api_key,
            "ivp_amount": post.get('amount') and round(float(post.get('amount')), 2),
            "ivp_currency": post.get('currency'),
            # "ivp_test": 0 if acquirer.environment == 'prod' else 1,
            "ivp_cart": sequence or "NEW",
            "ivp_appleay": 1,
            # "ivp_cart": post.get('reference'),
            "ivp_desc": "Payment from odex With Reference : %s" % post.get('reference'),
            "return_auth": '%s?reference=%s' % (urls.url_join(base_url, '/payment/telr/return'), post.get('reference')),
            "return_decl": '%s?reference=%s' % (urls.url_join(base_url, '/payment/telr/return'), post.get('reference')),
            "return_can": '%s?reference=%s' % (urls.url_join(base_url, '/payment/telr/return'), post.get('reference')),
            "bill_fname": partner_id.name,
        }
        if partner_id.street:
            payload["bill_addr1"] = partner_id.street,
        if partner_id.city:
            payload["bill_city"] = partner_id.city,
        if partner_id.country_id:
            payload["bill_country"] = partner_id.country_id.name,
        if partner_id.email:
            payload["bill_email"] = partner_id.email,
        if partner_id.phone:
            payload["bill_phone"] = partner_id.phone,

        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response_data = requests.request("POST", url, data=payload, headers=headers)
        response = json.loads(response_data.text)
        _logger.info('Telr: response telr data %s', response)

        if not response.get('order'):
            return werkzeug.utils.redirect('/shop')
        else:
            TX.telr_order_id = response.get('order').get('ref')
            request.session['telr_order_id'] = TX.telr_order_id
            return werkzeug.utils.redirect(response.get('order').get('url'))

    @http.route(_return_url, type='http', auth='public', methods=['GET'], csrf=False, save_session=False)
    def telr_return_from_redirect(self, **post):
        post.update({'cartid': post.get('reference')})
        tx = request.env['payment.transaction'].sudo()._telr_form_get_tx_from_data(post)
        telr_order_id = request.session.get('telr_order_id')
        post.update(tx._get_telr_tx_status(telr_order_id))
        _logger.info('Telr: entering form_feedback with post data %s', pprint.pformat(post))
        request.env['payment.transaction'].sudo().form_feedback(post, 'telr')
        request.session['telr_order_id'] = None
        return werkzeug.utils.redirect('/shop/payment/validate')

class WebsiteSaleTelr(WebsiteSale):

    @http.route('/shop/payment/validate', type='http', auth="public", website=True, sitemap=False)
    def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
        res = super().payment_validate(transaction_id=transaction_id, sale_order_id=sale_order_id)
        if sale_order_id is None:
            order = request.website.sale_get_order()
            if not order and 'sale_last_order_id' in request.session:
                last_order_id = request.session['sale_last_order_id']
                order = request.env['sale.order'].sudo().browse(last_order_id).exists()
        else:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            assert order.id == request.session.get('sale_last_order_id')
        if order.state != 'cancel':
            if order.state in ['draft', 'sent']:
                order.action_confirm()
            order._create_invoices(final=True)
            order.invoice_ids.action_post()
            for invoice in order.invoice_ids:
                request.env['account.payment.register'] \
                    .sudo().with_context(active_model='account.move', active_ids=invoice.ids) \
                    .create({}) \
                    ._create_payments()

        return res
