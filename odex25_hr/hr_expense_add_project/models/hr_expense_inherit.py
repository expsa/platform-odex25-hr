from odoo import fields, models, api,_


class HRExpensw(models.Model):
    _inherit = 'hr.expense'

    project_id  = fields.Many2one(comodel_name='project.project', string=_('Project'))
    
    analytic_account_id = fields.Many2one(related='project_id.analytic_account_id', string='Analytic Account', check_company=True)
