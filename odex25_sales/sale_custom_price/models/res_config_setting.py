from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    prevent_selling = fields.Boolean(string='Prevent Selling',
                                     config_parameter='sale_custom_price.prevent_selling')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            prevent_selling=self.env['ir.config_parameter'].sudo().get_param('sale_custom_price.prevent_selling')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('sale_custom_price.prevent_selling', self.prevent_selling)
