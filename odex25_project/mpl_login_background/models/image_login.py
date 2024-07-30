from odoo import models, fields, api, _


class LoginImage(models.Model):
    _name = 'image.login'
    _description = 'Image Login'
    _rec_name = 'name'

    image = fields.Binary(string="Image")
    name = fields.Char(string="Name")
