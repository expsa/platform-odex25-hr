# -*- coding: utf-8 -*-
from ast import literal_eval

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    terms_id = fields.Many2one(comodel_name='sale.terms.conditions', string='Default Term', default_model='sale.terms.conditions')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].set_param
        set_param('terms_id', (self.terms_id.id or False))

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        term_id = literal_eval(get_param('terms_id', default='False'))
        res.update(
            terms_id=term_id,
        )
        return res


