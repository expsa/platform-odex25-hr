# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

import json
import logging
import pprint

import requests
import werkzeug
from werkzeug import urls

from odoo import http, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.http import request
from odoo.exceptions import UserError, Warning

_logger = logging.getLogger(__name__)


class ApplepayController(http.Controller):

    @http.route('/payment/applepay/return', type='http', auth='public', csrf=False)
    def applepay_return(self, **post):
        """ applepay."""
        acquirer = request.env['payment.acquirer'].sudo().search([('provider', '=', 'applepay')], limit=1)
        print("acquirer......applepay", acquirer.state)
        if post.get('resourcePath'):
            if acquirer.state == 'test':
                url = "https://test.oppwa.com"
            else:
                url = "https://oppwa.com"
            url += post.get('resourcePath')
            url += '?entityId=' + acquirer.applepay_entity_id
            authorization_bearer = "Bearer " + acquirer.applepay_authorization_bearer
            try:
                headers = {'Authorization': authorization_bearer}

                response = requests.get(
                    url,
                    headers=headers,
                )
                response = json.loads(response.text)
            except Exception as e:
                raise UserError(_(e))
            _logger.info(
                'applepay: entering form_feedback with post data %s', pprint.pformat(post))
            request.env['payment.transaction'].sudo().form_feedback(response, 'applepay')
        return werkzeug.utils.redirect('/payment/process')

    @http.route('/shop/applepay/payment/', type='http', auth="none", csrf=False)
    def _payment_applepay_card(self, **kw):
        acquirer = request.env['payment.acquirer'].sudo().search([('provider', '=', 'applepay')], limit=1)
        if acquirer.state == 'test':
            return request.render("payment_applepay.payment_applepay_card",
                                  {'check_out_id': kw.get('check_out_id'), 'return_url': kw.get('hyperpay_return')})
        else:
            return request.render("payment_applepay.payment_applepay_card_live",
                                  {'check_out_id': kw.get('check_out_id'), 'return_url': kw.get('hyperpay_return')})
