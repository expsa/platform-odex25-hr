# -*- coding: utf-8 -*-
from odoo import models, fields


class TermsConditions(models.Model):
    _name = 'sale.terms.conditions'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    default_term = fields.Boolean(string='Default Term')
    desc = fields.Html(string='Description', translate=True)


