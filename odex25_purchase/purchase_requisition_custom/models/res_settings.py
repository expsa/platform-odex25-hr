from odoo import fields, models


class ResSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    # todo start
    # add new purchase setting
    chief_executive_officer = fields.Float(string='Chief Executive Officer', readonly=False, related="company_id.chief_executive_officer")
    direct_purchase = fields.Float(string='Direct Purchase Amount', readonly=False, related="company_id.direct_purchase")
    exceptional_amount = fields.Float(string='Exceptional Amount', readonly=False, related="company_id.exceptional_amount")
# todo end
    second_approve = fields.Integer(string='second approve', related="company_id.second_approve", readonly=False)
    # third_approve = fields.Integer(string='third approve' , related="company_id.third_approve")
    purchase_budget = fields.Boolean(string='Purchase budget', related="company_id.purchase_budget", readonly=False)
    purchase_analytic_account = fields.Many2one('account.analytic.account',
                                                related="company_id.purchase_analytic_account", readonly=False)

    # def get_values(self):
    #     res = super(ResSetting, self).get_values()

    #     res['second_approve'] = int(self.env['ir.config_parameter'].sudo().get_param('purchase_requisition_custom.second_approve', default=0))

    #     return res

    # @api.model
    # def set_values(self):
    #     self.env['ir.config_parameter'].sudo().set_param('purchase_requisition_custom.second_approve', self.second_approve)

    #     super(ResSetting, self).set_values()