from odoo import _, api, fields, models

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    priority = fields.Selection([('3', 'A'),('2', 'B'),('1', 'C') ], string='Priority')

class MaintenanceTeam(models.Model):
    _inherit = 'maintenance.team'
    department_id = fields.Many2one('hr.department', string='Department',)

class MaintenanceEquipmentRequest(models.Model):
    _inherit = 'maintenance.request'
    # @api.model
    # def get_team(self):
    #     print("im here===================",self.env['maintenance.team'].search([('department_id','=',self.department_id.id)]))
    #     return self.env.['maintenance.team'].search([('department_id','=',self.department_id.id)]).member_ids.ids

    dis_priority = fields.Selection(
    related='equipment_id.priority',
    readonly=True,
    store=True,
    string='Priority'
    )
    # maintenance_team_id = fields.Many2one('maintenance.team', string='Team', check_company=True,
    # related='department_id.team_id',
    # readonly=True,
    # store=True
    # )

    # team_ids = fields.Many2many('res.users', string='Team',default=get_team)
    @api.onchange('employee_id','user_id','department_id')
    def _onchange_department_id_user_id(self):
        if self.department_id:
            teams = self.env.get('maintenance.team').search([('department_id','=',self.department_id.id)])
            member_ids = teams and teams.member_ids.ids or []
            domain = [('id','in',member_ids)]
            return {
                'value' : {'user_id' : False, 'maintenance_team_id' : teams and teams[0].id or False },
                'domain' : {
                    'user_id' : domain
                }
            }
        return {'value' : {'maintenance_team_id' : False, 'user_id' : False}, 'domain' : {'user_id' : [('id', '=', False)]}}
    


