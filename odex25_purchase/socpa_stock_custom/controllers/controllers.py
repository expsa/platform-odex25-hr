# -*- coding: utf-8 -*-
from odoo import http

# class SocpaStockCustom(http.Controller):
#     @http.route('/socpa_stock_custom/socpa_stock_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/socpa_stock_custom/socpa_stock_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('socpa_stock_custom.listing', {
#             'root': '/socpa_stock_custom/socpa_stock_custom',
#             'objects': http.request.env['socpa_stock_custom.socpa_stock_custom'].search([]),
#         })

#     @http.route('/socpa_stock_custom/socpa_stock_custom/objects/<model("socpa_stock_custom.socpa_stock_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('socpa_stock_custom.object', {
#             'object': obj
#         })