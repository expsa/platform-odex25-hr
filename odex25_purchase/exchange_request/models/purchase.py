# -*- coding: utf-8 -*-

from odoo import fields, models


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    exchange_request = fields.Many2one('exchange.request')


class PurchaseOrderCustom(models.Model):
    _inherit = "purchase.order"

    def action_confirm(self):
        """
            Make Purchase requisition done
        """
        if self.request_id:
            self.request_id.state = 'done'
        self.button_confirm()
