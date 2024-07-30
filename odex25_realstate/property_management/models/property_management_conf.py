# -*- coding: utf-8 -*-


from odoo import models, fields, api, exceptions, tools, _


class RentType(models.Model):
    _name = 'rent.type'
    _description = 'Rent Type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    active = fields.Boolean(default=True)
    name = fields.Char(string="Name")
    months = fields.Char(string="Months Between Payment")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id)

    _sql_constraints = [
        ('name_months', 'unique(name,months)', _('Name and months numbers must be unique.')),
    ]
