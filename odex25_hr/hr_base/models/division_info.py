# -*- coding: utf-8 -*-

from odoo import fields, models


class DivisionInfo(models.Model):
    _name = "division.info"
    _description = "Division Info"
    _rec_name = "division"

    company_name = fields.Many2one(comodel_name="res.company", string="Company Name", required=True)
    branch_name = fields.Many2one(comodel_name="res.company", string="Branch Name")
    division = fields.Char("Division", required=True)
