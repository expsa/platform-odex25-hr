# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class PurcahseRefues(models.TransientModel):
  

    _name = "purchase.request.cancel.wizard"
    _description = "purchase refuse Reason wizard"

    reason = fields.Text(string='Cancel Request Reason', required=True)
    request_id = fields.Many2one('purchase.request')
    user_id = fields.Many2one('res.users', string='Scheduler User', default=lambda self: self.env.user, required=True)

    @api.model
    def default_get(self, fields):
        res = super(PurcahseRefues, self).default_get(fields)
        active_ids = self.env.context.get('active_ids', [])
      
        res.update({
            'request_id': active_ids[0] if active_ids else False,
        })
        return res

    def request_cancel_reason(self):
        self.ensure_one()
        self.request_id.write({'state':'refuse','cancel_reason':self.reason,'user_id':self.user_id.id})
        return {'type': 'ir.actions.act_window_close'}
