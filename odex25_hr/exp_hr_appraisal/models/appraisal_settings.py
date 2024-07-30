from odoo import api, fields, models, _, exceptions
from datetime import date


class EmployeesAppraisal(models.Model):
    _name = 'appraisal.setting'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Appraisal'
    _rec_name = 'department_id'

    date = fields.Date()
    state = fields.Selection([("draft", _("Draft")),
                              ("appraisal", _("Appraisal Created"))], default='draft', tracking=True)
    department_id = fields.Many2one('hr.department')
    manager_id = fields.Many2one('hr.employee', related='department_id.manager_id')
    employee_ids = fields.Many2many('hr.employee')
    appraisal_plan_id = fields.Many2one('appraisal.plan')
    appraisal_id = fields.Many2one('hr.group.employee.appraisal')
    appraisal_type = fields.Selection(selection=[('performance', 'Performance'),
                                                 ('trial', 'Trial Period'),
                                                 ('training', 'Training'),
                                                 ('mission', 'Mission'),
                                                 ('general', 'General'),
                                                 ('other', 'Other')], string='Appraisal Type')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.model
    def create_automatic_appraisal(self):
        appraisal = self.search([])
        today = fields.Date.today()
        for rec in appraisal:
            if rec.date == today and rec.state != 'appraisal' or not rec.appraisal_id:
                appraisal_line = {
                    'date': rec.date,
                    'department_id': rec.department_id.id,
                    'manager_id': rec.manager_id.id,
                    'appraisal_plan_id': rec.appraisal_plan_id.id,
                    'appraisal_type': rec.appraisal_type,
                    'employee_ids': rec.department_id.member_ids.filtered(lambda emp: emp.state == 'open').ids,
                }
                line = self.env['hr.group.employee.appraisal'].create(appraisal_line)
                rec.write({'appraisal_id': line.id})
                for item in line:
                    if item.employee_ids:
                        appraisal_lines = []
                        # Fill employee appraisal
                        for element in item.employee_ids:
                            standard_appraisal_list, manager_appraisal_list = [], []

                            if not item.appraisal_plan_id.is_manager:
                                # Fill standard_appraisal_employee_line_ids to complete
                                for line in item.appraisal_plan_id.standard_appraisal_id:
                                    standard_appraisal_list.append({
                                        'great_level': line.great_level,
                                        'question': line.question
                                    })
                            else:
                                # Fill manager_appraisal_line_id to complete
                                for line in item.appraisal_plan_id.manager_appraisal_id:
                                    complete_manager_appraisal_list = []
                                    for record in line.question_id.customize_appraisal_id:
                                        complete_manager_appraisal_list.append({
                                            'question': record.question,
                                            'great_degree_level': record.great_degree_level,
                                            'degree_id': record.degree_id.id
                                        })
                                    record = self.env['manager.appraisal.complete.line'].create({
                                        'name': line.question_id.name,
                                        'great_level': line.great_level,
                                        'customize_appraisal_id': [(0, 0, value) for value in
                                                                   complete_manager_appraisal_list]
                                    })
                                    manager_appraisal_list.append({
                                        'appraisal_name': line.appraisal_name,
                                        'question_id': line.question_id.id,
                                        'question_complete_id': record.id
                                    })
                            appraisal_line = {
                                'employee_id': element.id,
                                'appraisal_date': date.today(),
                                'is_manager': item.appraisal_plan_id.is_manager,
                                'appraisal_plan_id': item.appraisal_plan_id.id,
                                'appraisal_type': item.appraisal_type,
                                'standard_appraisal_employee_line_ids': [(0, 0, value) for value in
                                                                         standard_appraisal_list],
                                'manager_appraisal_line_id': [(0, 0, value) for value in manager_appraisal_list]}
                            line_id = self.env['hr.employee.appraisal'].create(appraisal_line)

                            # Initialize
                            total_greed, total_great_level, line_id.level_achieved, line_id.great_level = 0.0, 0.0, 0.0, 0.0
                            appraisal_result_list = []

                            if not line_id.is_manager:
                                for line in line_id.standard_appraisal_employee_line_ids:
                                    # Update level achieved values when changed in lines
                                    total_greed += line.greed
                                    total_great_level += line.great_level
                                line_id.great_level = total_great_level
                                line_id.level_achieved = total_greed

                                # Update level achieved percentage when changed in lines
                                if line_id.level_achieved > 0.0 and line_id.great_level > 0.0:
                                    line_id.level_achieved_percentage = (
                                                                                line_id.level_achieved * 100) / line_id.great_level

                                # Determine which appraisal result from appraisal percentage
                                appraisal_result = self.env['appraisal.result'].search([
                                    ('result_from', '<', line_id.level_achieved_percentage),
                                    ('result_to', '>=', line_id.level_achieved_percentage)])

                                if len(appraisal_result) > 1:
                                    for line in appraisal_result:
                                        appraisal_result_list.append(line.name)
                                    raise exceptions.Warning(
                                        _('Please check appraisal result configuration , there is more than result for '
                                          'percentage %s  are %s ') % (
                                            round(line_id.level_achieved_percentage, 2), appraisal_result_list))
                                else:
                                    line_id.appraisal_result = appraisal_result.id

                            elif line_id.is_manager:
                                for line in line_id.manager_appraisal_line_id:
                                    # Update level achieved values when changed in lines
                                    total_greed += line.total
                                    total_great_level += line.great_level
                                line_id.great_level = total_great_level
                                line_id.level_achieved = total_greed

                                # Update level achieved percentage when changed in lines
                                if line_id.level_achieved > 0.0 and line_id.great_level > 0.0:
                                    line_id.level_achieved_percentage = (
                                                                                line_id.level_achieved * 100) / line_id.great_level

                                # Determine which appraisal result from appraisal percentage
                                appraisal_result = self.env['appraisal.result'].search([
                                    ('result_from', '<', line_id.level_achieved_percentage),
                                    ('result_to', '>=', line_id.level_achieved_percentage)])

                                if len(appraisal_result) > 1:
                                    for line in appraisal_result:
                                        appraisal_result_list.append(line.name)
                                    raise exceptions.Warning(
                                        _('Please check appraisal result configuration , there is more than result for '
                                          'percentage %s  are %s ') % (
                                            round(line_id.level_achieved_percentage, 2), appraisal_result_list))
                                else:
                                    line_id.appraisal_result = appraisal_result.id
                            appraisal_lines.append(line_id.id)
                        item.appraisal_id = self.env['hr.employee.appraisal'].browse(appraisal_lines)
                    else:
                        raise exceptions.Warning(_('Please select at least one employee to make appraisal.'))
                    item.state = 'gen_appraisal'

            rec.state = 'appraisal'
