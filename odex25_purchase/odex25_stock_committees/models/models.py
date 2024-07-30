# -*- coding: utf-8 -*-
from odoo import models, fields, api
class StockInventoryCommittees(models.Model):
    _name = 'inventory.committees'
    _description = 'Inventory Committees'
    name = fields.Char('Committee Name',required=True)
    responsiple_id = fields.Many2one(comodel_name='res.partner',string='Responsiple Committee')
    members_ids = fields.One2many( comodel_name='res.members', inverse_name='inventory_committees_id', string='Committees Members')
class ItemReturnCommittees(models.Model):
    _name = 'item.return.committees'
    _description = 'Item Return Committees'
    name = fields.Char('Committee Name',required=True)
    responsiple_id = fields.Many2one(comodel_name='res.partner',string='Responsiple Committee')
    members_ids = fields.One2many(comodel_name='res.members',inverse_name='item_return_committees_id',string='Committees Members')
class ItemDestructionCommittees(models.Model):
    _name = 'item.destrcution.committees'
    _description = 'Item Destrcution Committees'
    name = fields.Char('Committee Name',required=True)
    responsiple_id = fields.Many2one(comodel_name='res.partner',string='Responsiple Committee')
    members_ids = fields.One2many(comodel_name='res.members',inverse_name='item_destruction_committees_id',string='Committees Members')
class MemberCommittees(models.Model):
    _name = 'res.members'
    member_id  = fields.Many2one(comodel_name='res.users',string='Name')
    login = fields.Char(store=True,readonly=False,related='member_id.login',required=True, help="Used to log into the system")
    login_date = fields.Datetime(store=True,readonly=False,related='member_id.login_date', string='Latest authentication',)
    totp_enabled = fields.Boolean(store=True,readonly=False,string="Two-factor authentication",related='member_id.totp_enabled',)
    lang = fields.Selection(store=True,readonly=False,related='member_id.lang',selection='_get_languages', string='Language', validate=False)
    inventory_committees_id  = fields.Many2one(comodel_name='inventory.committees',)
    item_destruction_committees_id  = fields.Many2one(comodel_name='item.destrcution.committees',)
    item_return_committees_id  = fields.Many2one(comodel_name='item.return.committees',)
    @api.model
    def _get_languages(self):
        return self.env['res.lang'].get_installed()
    # @api.depends('totp_secret')
    # def _compute_totp_enabled(self):
    #     for r, v in zip(self, self.sudo()):
    #         r.totp_enabled = bool(v.totp_secret)



