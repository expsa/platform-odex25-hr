# -*- coding: utf-8 -*-
from ast import literal_eval

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    terms_id = fields.Many2one(comodel_name='sale.terms.conditions', string='Terms&Conditions')
    terms_desc = fields.Html(compute='_get_terms_clean')
    note = fields.Html(string='Note')

    @api.depends('terms_id')
    def _get_terms_clean(self):
        for item in self:
            if item.terms_id and item.terms_id.desc:
                if len(item.terms_id.desc) > 200:
                    item.terms_desc = item.terms_id.desc[:200] + '...........'
                else:
                    item.terms_desc = item.terms_id.desc + '...........'
            else:
                item.terms_desc = ' '

    @api.onchange('terms_id')
    def onchange_terms_ids_change(self):
        for rec in self:
            if rec.terms_id:
                rec.note = rec.terms_id.desc

    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        default_term = self.env['sale.terms.conditions'].sudo().search([('default_term', '=', True)], limit=1,
                                                                       order='id desc')
        get_param = self.env['ir.config_parameter'].sudo().get_param
        use_sale_note = get_param('sale.use_sale_note')
        term_id = literal_eval(get_param('default_terms_id', default='False'))
        if use_sale_note:
            res['terms_id'] = term_id
        elif default_term:
            res['terms_id'] = default_term.id
        else:
            res['terms_id'] = False
        return res



