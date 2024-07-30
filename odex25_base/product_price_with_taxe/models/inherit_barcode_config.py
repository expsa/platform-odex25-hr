from odoo import models, fields, api


class BarcodeConfig(models.Model):
    _inherit = 'barcode.configuration'

    price_ht_display = fields.Boolean('Price without Tax', default=False)
