# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class POSConfig(models.Model):
    _inherit = 'pos.config'

    print_by_branch = fields.Boolean('Branch Invoice')
