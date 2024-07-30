from odoo import _, api, fields, models
from datetime import datetime, timedelta, time
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from lxml import etree
import simplejson #If not installed, you have to install it by executing pip install simplejson


class MaintenanceFailure(models.Model):
    _name = 'maintenance.failure'

    name = fields.Char('Name', required=True)
    user_ids = fields.Many2many('res.users', 'failure_supervisor_rel', string='Engineers')


class MaintenanceSpare(models.Model):
    _name = 'maintenance.request.spare'

    spare_id = fields.Many2one('product.template', string='Spare', domain=[('is_spare', '=', True)])
    quantity = fields.Integer('Quantity')
    cost = fields.Float('Cost')
    request_id = fields.Many2one('maintenance.request', string='Related Request')
    total = fields.Float('Total', readonly=True, compute='_compute')

    @api.depends('quantity', 'cost')
    def _compute(self):
        for rec in self:
            rec.total = rec.cost * rec.quantity
    
    @api.onchange('spare_id')
    def onchange_spare(self):
        self.cost = self.spare_id.standard_price

class MaintenanceSpare(models.Model):
    _name = 'maintenance.rootfailure'

    name = fields.Char('Description')

class MaintenanceRequestTask(models.Model):
    _name = 'maintenance.request.task'

    name = fields.Char('name')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    time = fields.Float('Executing Time')
    duration = fields.Float('Duration')
    is_done = fields.Boolean('Complete ?')
    request_id = fields.Many2one('maintenance.request', 'Maintenance Request')


class MaintenanceEquipmentRequest(models.Model):
    _inherit = 'maintenance.request'

    code = fields.Char('Request No',  default='/')
    failure_id = fields.Many2one('maintenance.failure', string='Failure Type')
    tool_ids = fields.Many2many('product.template', 'maintenance_tool_rel', string="Tools", domain=[('is_tool', '=', True)])
    spare_ids = fields.One2many('maintenance.request.spare', 'request_id', string="Spares")
    maintenance_team_id = fields.Many2one('maintenance.team', string='Team', check_company=True,)
    stage_type = fields.Selection(string='Stage Type', related='stage_id.stage_type')
    team_type = fields.Selection([('in', 'Internal Team'), ('out', 'Outsite Entity')], 'Team Type')
    out_entity_id = fields.Many2one('res.partner', 'Entity', domain=[('is_company', '=', True)])
    request_date = fields.Datetime('Request Date', tracking=True, default=fields.Datetime.now,
                               help="Date requested for the maintenance to happen")
    dis_employee_ids = fields.Many2many('hr.employee', 'dis_req_member_rel', string='Team Members')    
    employee_ids = fields.Many2many('hr.employee', 'req_member_rel', string='Team Members')
    failure_desc = fields.Text('Failure Description')
    failure_cause_id = fields.Many2one('maintenance.rootfailure', string='Failure Root Cause')
    maintenance_work = fields.Text('Maintenance works')
    dis_priority = fields.Selection([('3', 'A'),('2', 'B'),('1', 'C') ], string='Priority')
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    maintenance_time = fields.Float('Maintenance Duration')
    estimated_time = fields.Float('Estimated Duration')
    task_ids = fields.One2many('maintenance.request.task', 'request_id', string='Tasks')
    attachment = fields.Binary(string="Instruction Document", attachment=True)
    done_time = fields.Datetime('Complete Time')
    start_time = fields.Datetime('Maintenance Begin Time')
    entry_source = fields.Selection([('request','Request Order'),('order', 'Order Request'), ('job', 'Equipment Job')], string='Source', default='request')
    machine_status = fields.Selection([('out_service', 'Out of Service'),('part','Partially effect'),('in_service','In Service')], string='Machine Status')
    maintenance_category = fields.Selection([('planned', 'Planned'), ('unplanned', 'Unplanned')], string="Maintenance category ")
    down_time = fields.Float('Down Time')
    product_loss = fields.Float('losses of production')
    department_id = fields.Many2one('hr.department', string='Department',
    related='employee_id.department_id',
    readonly=True,
    store=True
    )

    
    # @api.onchange('stage_id')
    # def _onchange_stage_id(self):
    #     # print("iam here=================",self.stage_id.sequence)
    #     now = datetime.now()
    #     if self.stage_id.stage_type == 'confirm':
    #         self.request_date = now
    #         self.fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False)
    
    
  
    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     """
    #     Overrides orm field_view_get.
    #     @return: Dictionary of Fields, arch and toolbar.
    #     """

    #     res = super(MaintenanceEquipmentRequest, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     print("self.env.context============================",self.env.context)
    #     # if doc.xpath("//field[@name='city_id']")
    #     if self.env.context:  # Check for context value
    #         doc = etree.XML(res['arch']) #Get the view architecture of record
    #         if view_type == 'form': # Applies only if it is form view
    #             print("here---------------------")
    #             for node in doc.xpath("//field"): #Get all the fields navigating through xpath  
    #                 print("fields===========================node",node.get("name"))
    #                 modifiers = simplejson.loads(node.get("modifiers")) #Get all the existing modifiers of each field
    #                 modifiers['readonly'] = True #Add readonly=True attribute in modifier for each field
    #                 node.set('modifiers', simplejson.dumps(modifiers)) #Now, set the newly added modifiers to the field
    #             res['arch'] = etree.tostring(doc) #Update the view architecture of record with new architecture
    #     return res
    

    @api.onchange('dis_employee_ids', 'user_id','team_type')
    def onchange_members(self):
        member_ids = []
        if self.user_id:
            res = self.env.get('hr.employee').search([('user_id','=',self.user_id.id)])
            if res : member_ids.append(res[0].id)
        if self.dis_employee_ids and self.team_type == 'in' :
            member_ids += self.dis_employee_ids.ids
        self.employee_ids = [(6, 0 , member_ids)]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('maintenance.request') or _('New')
        if 'dis_priority' in vals:
            vals['priority'] = vals['dis_priority']
        obj = super(MaintenanceEquipmentRequest, self).create(vals)
        obj.onchange_members()
        return obj

    # @api.onchange('failure_id','maintenance_type')
    # def onchange_failure(self):
    #     domain = [('id','>','0')]
    #     if self.maintenance_type == 'corrective':
    #         dom = self.failure_id and self.failure_id.user_ids.ids or []
    #         domain = [('id', 'in', dom)]
    #     return {
    #         'value' : {'user_id' : False},
    #         'domain' : {
    #             'user_id' : domain
    #         }
    #     }

    def write(self,vals):
        stage = self.env.get('maintenance.stage')
        user=self.env.user
        user_id = user.id
        if 'dis_priority' in vals:
            vals['priority'] = vals['dis_priority']
        if 'stage_id' in vals:
            new_value = vals['stage_id']
            old = self.stage_id
            new = stage.browse(new_value)
           

            if old.sequence > new.sequence:
                if  old.pre_stage_ids.ids  and new_value not in old.pre_stage_ids.ids:
                    raise UserError(_('You cannot use return back to this stage.'))
            else:
                if self.stage_id.next_stage_ids and  new_value not in self.stage_id.next_stage_ids.ids:
                    raise UserError(_('You cannot use go forword to this stage.'))
                

            
            if  new.stage_type == 'confirm':
                if 'employee_id' in vals:
                    em = vals['employee_id']
                    em_id = self.env.get('hr.employee').browse(em)
                    if user_id != em_id.user_id.id:
                        raise UserError(_('You cannot use confrim this request,only requester can perform this action'))
                else:
                    em_id = self.employee_id
                    if em_id and user_id != em_id.user_id.id:
                        raise UserError(_('You cannot use confrim this request,only requester can perform this action'))
                now = datetime.now()
                self.write({'request_date':now})

            if  new.stage_type == 'for_order':
                if self.user_id and self.user_id.id != user_id:
                    raise UserError(_('Only user who create the work order can perform this action'))
                teams = self.maintenance_team_id.member_ids.ids
                print("tems================",teams)
                if user_id not in teams:
                    print("in here===========")
                    raise UserError(_('Only team members for current department team can perform this action'))
                # if 'equipment_id' in vals:
                #     equipment = vals['equipment_id']
                #     equipment_id = self.env.get('maintenance.equipment').browse(equipment)
                #     if user_id not in equipment_id.maintenance_team_id.member_ids.ids:
                #         raise UserError(_('Only team members can perform this action'))
                # else:
                    
                #     if self.equipment_id and user_id not in self.equipment_id.maintenance_team_id.member_ids.ids:
                #         raise UserError(_('Only team members can perform this action'))
                self.write({'user_id':user_id})

            if new.stage_type == 'repair_done':
                if 'user_id' in vals:
                    usr = vals['user_id']
                    usr_id = self.env.get('res.users').browse(usr)
                    # teams = self.env.get('maintenance.team').search([('department_id','=',self.department_id.id)]).member_ids.ids
                    if usr_id and usr_id.id !=user_id :
                        raise UserError(_('You cannot use process this request,only supervisor can perform this action'))
                else:
                    usr_id = self.user_id
                    if usr_id and  usr_id.id != user_id:
                        raise UserError(_('You cannot use process this request,only supervisor can perform this action'))

            if new.stage_type == 'request_done':
                if 'employee_id' in vals:
                    em = vals['employee_id']
                    em_id = self.env.get('hr.employee').browse(em)
                    if user_id != em_id.user_id.id:
                        raise UserError(_('You cannot confirm this request,only requester can perform this action'))
                else:
                    em_id = self.employee_id
                    if em_id and user_id != em_id.user_id.id:
                        raise UserError(_('You cannot  confrim this request,only requester can perform this action'))
        return super(MaintenanceEquipmentRequest,self).write(vals)

class MaintenanceStage(models.Model) :
    _inherit = 'maintenance.stage'

    for_order = fields.Boolean('use for Order ?')
    stage_type = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confrim'),
        ('for_order','Orders'),
        ('repair_done','Repair Done'),
        ('request_done','Request Done'),
    ])
    
    next_stage_ids = fields.Many2many(
        string='Next Stage',
        comodel_name='maintenance.stage',
        relation='model_request_next_rel',
        column1='request_id',
        column2='stage_id',
    )

    pre_stage_ids = fields.Many2many(
        string='Previous Stage',
        comodel_name='maintenance.stage',
        relation='model_request_pre_rel',
        column1='request_id',
        column2='stage_id',
    )
    


class Product(models.Model) :
    _inherit = 'product.template'

    is_spare = fields.Boolean('Spare')
    is_tool = fields.Boolean('Tools')


class EquipmentMaintenaceTasks(models.Model):
    _name = 'maintenance.equipment.task'

    job_id = fields.Many2one('maintenance.equipment.job', string='Related Maintenance Job')
    name = fields.Char('Decription')
    sequence = fields.Integer('Sequence')


class EquipmentMaintenaceJob(models.Model):
    _name = 'maintenance.equipment.job'

    name = fields.Char('Decription')
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment')
    start_date = fields.Date('Maintenance Begin Date')
    next_action_date = fields.Date('Next Preventive')
    period = fields.Integer('Preventive Maintenance Frequency')
    period_type = fields.Selection([('hour', 'By Hour'), ('day', 'Daily'),('month','Monthly'),('year','Yearly')])
    maintenance_time = fields.Float('Maintenance Duration')
    user_id = fields.Many2one('res.users', string='supervisor')
    active = fields.Boolean('Active', default=True)
    task_ids = fields.One2many('maintenance.equipment.task', 'job_id', string='Tasks')
    attachment = fields.Binary(string="Instruction Document", attachment=True)

    @api.onchange('start_date')
    def onchange_start_date(self):
        self.next_action_date = self.start_date

    def write(self, vals):
        if 'start_date' in vals:
            vals['next_action_date'] = vals['start_date']
        return super(EquipmentMaintenaceJob, self).write(vals)


    @api.model
    def create(self, vals):
        if 'start_date' in vals:
            vals['next_action_date'] = vals['start_date']
        return super(EquipmentMaintenaceJob, self).create(vals)

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    
    job_ids = fields.One2many('maintenance.equipment.job', 'equipment_id')

    def create_maintenance_job(self):
        current_date = fields.Date.today()
        job_model = self.env.get('maintenance.equipment.job')
        res_job = job_model.search([('next_action_date', '=', current_date)])
        order_model = self.env.get('maintenance.request')
        res_stage = self.env.get('maintenance.stage').search([('stage_type','=','for_order')],order='sequence')
        stage_id = res_stage and res_stage[0].id or False
        for job in res_job:
            tasks = [(0,0,{'name' : t.name}) for t in job.task_ids]
            res_order = order_model.create({
                'name' : job.name,
                'user_id' : job.user_id.id,
                'stage_id' : stage_id,
                'maintenance_type' : 'preventive',
                'task_ids' : tasks,
                'attachment' : job.attachment,
                'entry_source' : 'job',
                'equipment_id' : job.equipment_id.id,
                'schedule_date' : current_date,
            })

class MaintenanceSummary(models.Model):
    _name = 'maintenance.summary'

    name = fields.Char('Description')
    total_orders = fields.Integer('Total Orders', compute='_compute_total')
    total_open = fields.Integer('Open', compute='_compute_total')
    total_repair = fields.Integer('Repaired', compute='_compute_total')
    total_close = fields.Integer('Closed', compute='_compute_total')
    order_chart = fields.Char('Maintenance Orders')
    priority_chart = fields.Char('Priority')
    total_low = fields.Integer('Low', compute='_compute_total')
    total_normal = fields.Integer('Normal', compute='_compute_total')
    total_high = fields.Integer('High', compute='_compute_total')
    planned_chart = fields.Char('Planned Maintenacne')
    total_planned = fields.Integer('Planned', compute='_compute_total')
    total_unplanned = fields.Integer('Un Planned', compute='_compute_total')
    total_partially_effect = fields.Integer('Total Partiall Effect', compute='_compute_total')
    total_downtime = fields.Integer('Total Downtime', compute='_compute_total')
    total_outservice = fields.Integer('Total Out of Service', compute='_compute_total')
    total_loss = fields.Integer('Loss of Production', compute='_compute_total')
    
    def _compute_total(self):
        order_model = self.env.get('maintenance.request')
        stage_model = self.env.get('maintenance.stage')
        stage_close = stage_model.search([('stage_type', '=', 'request_done')]).ids
        stage_repair = stage_model.search([('stage_type', '=', 'repair_done')]).ids
        stage_open = stage_model.search([('stage_type', 'not in', ['repair_done', 'request_done'])]).ids
        self.total_orders = order_model.search_count([])
        self.total_open = order_model.search_count([('stage_id', 'in', stage_open)])
        self.total_repair = order_model.search_count([('stage_id', 'in', stage_repair)])
        self.total_close = order_model.search_count([('stage_id', 'in', stage_close)])
        self.total_low = order_model.search_count([('priority', '=', 1)])
        self.total_normal = order_model.search_count([('priority', '=', 2)])
        self.total_high = order_model.search_count([('priority', '=', 3)])
        self.total_planned = order_model.search_count([('maintenance_category', '=', 'planned')])
        self.total_unplanned = order_model.search_count(['|',('maintenance_category', '=', 'unplanned'),('maintenance_category', '=', False)])
        self.total_partially_effect = order_model.search_count([('machine_status', '=', 'part')])
        self.total_outservice = order_model.search_count([('machine_status', '=', 'out_service')])
        total_loss = 0
        total_downtime = 0
        for req in order_model.search([('machine_status', '=', 'part')]):
            total_loss += req.product_loss
        for req in order_model.search([('machine_status', '=', 'out_service')]):
            total_downtime += req.down_time
        self.total_downtime = total_downtime
        self.total_loss = total_loss
