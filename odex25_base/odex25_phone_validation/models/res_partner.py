from odoo import api, models, _
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'
            
    @api.constrains('phone')
    def _check_unique_phone(self):
        for rec in self.filtered('phone'):
            res = self.search([('id', '!=', rec._origin.id), ('phone', '=', rec.phone)])
            if res:
                raise ValidationError(_(f'This phone number is already registered under contact {", ".join(res.mapped("name"))}'))