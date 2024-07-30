from odoo import models, fields, api

class PosConfig(models.Model):
    _inherit = 'pos.config'

    total_discount = fields.Boolean(default=True)
    total_discount_limit = fields.Float(default=0.0)