from odoo import api, models


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    def _prepare_default_reversal(self, move):
        res = super(AccountMoveReversal, self)._prepare_default_reversal(move)
        res.update({
            'discount_rate': move.discount_rate,
            'discount_type': move.discount_type,
        })
        return res
