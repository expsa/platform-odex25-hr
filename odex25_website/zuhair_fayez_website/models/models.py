# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    experiense_years = fields.Char(related='website_id.no_of_years', string='NO.Of Experiense Year')
    video_bg = fields.Char('Video', related='website_id.video_bg')


class Website(models.Model):
    _inherit = 'website'

    no_of_years = fields.Char('NO.Of Years Experiense')
    video_bg = fields.Char('Video Link')
