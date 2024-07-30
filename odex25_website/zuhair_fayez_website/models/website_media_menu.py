from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'website.media'
    _description = 'Media Menu'

    name = fields.Char()
    summary = fields.Text(string="Description")
    type = fields.Selection(
        string='Type',
        selection=[('news', 'News'), ('activity', 'Activities'),('achievements','Achievements') ],default='news')

