# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import UserError


class PosSession(models.Model):
    _inherit = 'pos.session'

    def action_pos_session_close(self):
        res = super().action_pos_session_close()
        if res.get('tag') == 'reload':
            return 'Success'
        return 'Fail'        


    def action_pos_session_closing_control(self):
        self._check_pos_session_balance()
        for session in self:
            if any(order.state == 'draft' for order in session.order_ids):
                raise UserError(_("You cannot close the POS when orders are still in draft"))
            if session.state == 'closed':
                raise UserError(_('This session is already closed.'))
            session.write({'state': 'closing_control', 'stop_at': fields.Datetime.now()})
            if not session.config_id.cash_control:
                session.with_delay(channel="root.pos_session").action_pos_session_close()
        return {
            'type': 'ir.actions.client',
            'name': 'Point of Sale Menu',
            'tag': 'reload',
            'params': {'menu_id': self.env.ref('point_of_sale.menu_point_root').id},
        }

    
    def action_pos_session_validate(self):
        self._check_pos_session_balance()
        return self.with_delay(channel="root.pos_session").action_pos_session_close()
