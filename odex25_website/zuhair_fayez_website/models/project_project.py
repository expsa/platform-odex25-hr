from odoo import fields, models, api


class ModelName(models.Model):
    _inherit = 'project.project'
    _description = 'Description'

    service_id = fields.Many2one(comodel_name='website.project.service', string='Service Name')
    website_image_ids = fields.One2many('website.image', 'project_id', string='Images')
    website_name  = fields.Char(string='Website Name')
    description_website = fields.Char(string='Description')
    image = fields.Binary(string="Main Image")

class WebsiteImage(models.Model):
    _name = 'website.image'

    name = fields.Char('Name')
    image = fields.Binary('Image', attachment=True)
    project_id = fields.Many2one('project.project', 'Related website', copy=True,invisable=True)
