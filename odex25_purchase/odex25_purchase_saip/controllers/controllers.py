# -*- coding: utf-8 -*-
# from odoo import http


# class Odex25PurchaseSaip(http.Controller):
#     @http.route('/odex25_purchase_saip/odex25_purchase_saip/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odex25_purchase_saip/odex25_purchase_saip/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odex25_purchase_saip.listing', {
#             'root': '/odex25_purchase_saip/odex25_purchase_saip',
#             'objects': http.request.env['odex25_purchase_saip.odex25_purchase_saip'].search([]),
#         })

#     @http.route('/odex25_purchase_saip/odex25_purchase_saip/objects/<model("odex25_purchase_saip.odex25_purchase_saip"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odex25_purchase_saip.object', {
#             'object': obj
#         })
