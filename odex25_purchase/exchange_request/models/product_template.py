# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    consumed_ok = fields.Boolean(string="Can be Consumed")
