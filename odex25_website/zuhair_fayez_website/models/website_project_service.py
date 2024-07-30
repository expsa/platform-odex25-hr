from odoo import models, fields, api


class WebsitePprojectService(models.Model):
    _name = 'website.project.service'
    _parent_store = True
    _parent_name = "parent_service_id"
    _order = "sequence, name"
    # optional if field is 'parent_id'
    name = fields.Char(string='Service Name')
    image = fields.Binary(string="Image")
    is_main = fields.Boolean(string='Is Main', default=True)
    parent_path = fields.Char(index=True)

    parent_service_id = fields.Many2one(ondelete='restrict', index=True, comodel_name='website.project.service',
                                        string='Parent Service')
    child_ids = fields.One2many(comodel_name='website.project.service', inverse_name='parent_service_id',
                                string='Child service')
    sequence = fields.Integer(help="Gives the sequence order when displaying a list of product categories.")


    @api.constrains('parent_service_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')
