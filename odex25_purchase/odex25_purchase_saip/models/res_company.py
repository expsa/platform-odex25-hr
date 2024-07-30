# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    attachment_booklet_exp = fields.Binary(
        string='file', readonly=False, attachment=True, help='Upload Booklet file')
#     # - How to implement business and service  طريقة تنفيذ الاعمال والخدمات
#     business_service = fields.Html('How to implement business and service')
# # - quality classification  مواصفات الجودة
#     quality_classification = fields.Html('quality classification')
# # - Security classification  مواصفات السلامة
#     security_classification = fields.Html('Security classification')
# # - Special Terms and Conditions الشروط الخاصة
#     special_terms_conditions = fields.Html('Special Terms and Conditions')
