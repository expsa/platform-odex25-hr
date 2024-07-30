from odoo import fields, models


class ResSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    attachment_booklet_exp = fields.Binary(string='file',readonly=False, related="company_id.attachment_booklet_exp", attachment=True, help='Upload Booklet file')


    
   