from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sequence = fields.Char(String="Sequence", required=True, copy=False, readonly=True,
                           index=True, default='New')

    @api.model
    def create(self, values):
        if values.get('sequence', 'New') == 'New':
            values['sequence'] = self.env['ir.sequence'].next_by_code('partner.sequence') or 'New'
        return super(ResPartner, self).create(values)

    def cron_action_to_update_old_sequence(self, field_name=False):
        if field_name and field_name != 'field_name':
            try:
                partner_ids = self.env['res.partner'].search([(field_name, '!=', False)])
            except:
                raise UserError(_("Wrong field name added to the function !"))
            for partner_id in partner_ids:
                partner_id.sequence = partner_id.read([field_name])[0].get(field_name, 'New')
        else:
            partner_ids = self.env['res.partner'].search([('sequence', '=', 'New')], order="id asc")
            for partner_id in partner_ids:
                partner_id.sequence = self.env['ir.sequence'].next_by_code('partner.sequence') or 'New'
