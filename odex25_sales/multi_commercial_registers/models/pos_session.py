# -*- coding: utf-8 -*-


from odoo import api, fields, models, _

import logging

_logger = logging.getLogger(__name__)


class PosSession(models.Model):
    _inherit = "pos.session"

    branch_registry = fields.Char(related='branch_id.branch_registry')
    # branch_logo = fields.Binary(related='branch_id.logo')
    branch_logo = fields.Binary(related='branch_id.logo')
    address = fields.Text(related='branch_id.address')

    print_by_branch = fields.Boolean(string='Branch Invoice', )

    @api.model
    def create(self, values):
        if values.get('config_id'):
            values['print_by_branch'] = self.env['pos.config'].browse(values.get('config_id')).print_by_branch
        return super(PosSession, self).create(values)


class PosOrder(models.Model):
    _inherit = "pos.order"

    print_by_branch = fields.Boolean(related='session_id.print_by_branch', )


