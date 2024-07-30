# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import ValidationError


class ResCompanyExt(models.Model):
    _inherit = 'res.company'

    # branch = fields.Char("Branch" ,required=True)
    # branch_t = fields.Char("Branch Tagline")
    english_name = fields.Char(string='English Name')
    flip = fields.Boolean("/ ")
    # sponsor_id = fields.Char(string="SponsorID",required=True)
    po_no = fields.Char(string="P.O Box No", )
    location = fields.Char(string="Location Code")

    company_link = fields.One2many('res.company.tree', 'company_id', string="License Documents")
    sponsor_link = fields.One2many('res.sponsor', 'sponsor_tree', string="Sponsors")
    hr_email = fields.Char(string='HR Email')
    hr_manager_id = fields.Many2one('hr.employee', string='HR Manager')
    saudi_percentage = fields.Integer(string='Saudi Percentage %')

    contract_end_reminder = fields.Integer(string='Contract End Reminder')
    contract_trial_reminder = fields.Integer(string='Contract Trial Reminder')

    saudi_gosi = fields.Float(string='Saudi Gosi', default=10)
    company_gosi = fields.Float(string='Company Gosi', default=12)
    none_saudi_gosi = fields.Float(string='None Saudi Gosi', default=2)

    @api.constrains('saudi_percentage')
    def saudi_percentage_less_100(self):
        for item in self:
            if item.saudi_percentage > 100:
                raise ValidationError(_('The percentage should not exceed 100%'))


class ResCompanyExtTree(models.Model):
    _name = 'res.company.tree'
    _description = 'Company Tree'

    doc_type = fields.Many2one(comodel_name='documents.typed', string="Doc Type")
    issue_date = fields.Date("Issue Date", required=True)
    latest_renewal_date = fields.Date("Latest Renewal Date")
    expiry_date = fields.Date("Expiry Date", required=True)
    renewal = fields.Date("Due for Renewal", required=True)

    company_id = fields.Many2one(comodel_name='res.company')


class Sponsor(models.Model):
    _name = 'res.sponsor'
    _description = 'Sponsor'

    name = fields.Char(string='Sponsor Name', required=True, store=True)
    sponsor_id = fields.Integer(string='Sponsor ID', required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Contact Person', required=True)
    cr_no = fields.Char(string='CR No')
    street = fields.Char()
    street2 = fields.Char()
    zip_code = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one(comodel_name='res.country.state', string="Fed. State")
    country_id = fields.Many2one(comodel_name='res.country', string="Country")
    pob = fields.Char(string='P.O Box No')
    email = fields.Char(related='partner_id.email', store=True, readonly=True)
    phone = fields.Char(related='partner_id.phone', store=True)
    website = fields.Char(related='partner_id.website', readonly=True)
    fax = fields.Char(string="Fax")
    mobile = fields.Char(string='Mobile No')

    sponsor_tree = fields.Many2one(comodel_name='res.company')

    @api.onchange('state_id')
    def _onchange_state(self):
        self.country_id = self.state_id.country_id


class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    saudi_percentage = fields.Integer(string='Saudi Percentage %', related='company_id.saudi_percentage', readonly=False)
    contract_end_reminder = fields.Integer(string='Contract End Reminder',
                                           related='company_id.contract_end_reminder', readonly=False)
    contract_trial_reminder = fields.Integer(string='Contract Trial Reminder',
                                             related='company_id.contract_trial_reminder', readonly=False)
    saudi_gosi = fields.Float(string='Saudi Gosi', related='company_id.saudi_gosi', readonly=False)
    company_gosi = fields.Float(string='Company Gosi', related='company_id.company_gosi', readonly=False)
    none_saudi_gosi = fields.Float(string='None Saudi Gosi', related='company_id.none_saudi_gosi', readonly=False)


class ResCountryExt(models.Model):
    _inherit = 'res.country'

    english_name = fields.Char(string='English Name')
