# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Branch(models.Model):
    _inherit = 'res.branch'

    website = fields.Char(string="Website")
    po_no = fields.Char(string="P.O Box No")
    location = fields.Char(string="Location Code")
    email = fields.Char(string="Email")
    hr_email = fields.Char(string="HR Email")
    vat = fields.Char(related="company_id.vat")
    branch_registry = fields.Char(string="Branch Registry", store=True)
    currency_id = fields.Many2one('res.currency', string="Currency")
    report_footer = fields.Text(string="Report Footer")
    report_header = fields.Text(string="Company Tagline")
    partner_id = fields.Many2one('res.partner', string="Partner")
    social_twitter = fields.Char('Twitter Account')
    social_facebook = fields.Char('Facebook Account')
    social_github = fields.Char('Github Account')
    social_linkedin = fields.Char('LinkedIn Account')
    social_youtube = fields.Char('Youtube Account')
    social_googleplus = fields.Char('Google+ Account')
    logo = fields.Binary(string="Branch Logo")
    telephone_no = fields.Char(string='Telephone No')

    street = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one('res.country.state')
    country_id = fields.Many2one('res.country')

    