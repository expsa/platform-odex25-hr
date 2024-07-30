# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    state = fields.Selection(
        selection_add=[('draft', _('Draft')),
                       ('procurement_unit', _('Procurement Unit')),
                       ('dm', _('Chief Executive Officer')),
                       ('ppmo', _('Performance & planing Management officer')),
                       ('ppmm', _('Performance & planing Management manager')),
                       ('dm1', _('Chief Executive Officer')),
                       ('CSO', _('Chief Strategy Officer-CSO')),
                       ('direct_manager', _('Technical Department')),
                       ('send_budget', _('Budget Management')),
                       ('wait_budget', _('Pending Budget Approve')),
                       ('procurement', _('Procurement Manager')),
                       ('chairman_vision_office', _('Chairman Vision Office Committee')),
                       ('ceo_purchase', _('Executive Director of Procurement and Contracts')),
                       ('budget_approve', _('Executive Vice President of Corporate Resources')),
                       ('general_supervisor', _('Chief Procurement Executive')),
                       ('waiting', _('Procurement Department')),
                       ('done', _('Done')),
                       ('cancel', _('Cancel')),
                       ('refuse', _('Refuse'))], default="draft", tracking=True)

    purchase_request_type = fields.Selection([
        ('initiative', 'Initiative Purchaser Rquest'),
        ('ordinary', 'Ordinary Purchase Request'),
        ('emarket', 'E-market Purchase Request'),
        ('strategy','National Strategy Purchase Request')
    ], string='Purchase Request Type')

    project_name = fields.Char('Project Name')
    sub_project = fields.Char('Sub Project')
    project_duration = fields.Char('Project Duration')
    strategic_objective = fields.Selection([
        ('e_d_p', '3.1.1 Ease of doing business'),
        ('a_f_d_i', '3.1.6 Attracting foreign direct investment'),
        ('d_r_s', '3.3.5 Development of the retail sector'),
        ('i_c_e', '4.3.2 Increasing SMEs contribution to the economy'),
        ('other', 'Other')
    ], string='Strategic Objective')

    other_strategic_objective = fields.Char('Other Strategic objective')
    vision_program_name = fields.Char('Vision Program Name')
    initiative_name = fields.Char('Initiative Name')
    initiative_end_date = fields.Date('Initiative End Date')
    is_direct_manager = fields.Boolean('Sent Technical Department')
    cso_agreed = fields.Selection([
        ('agreed', 'Agreed'),
        ('not_agreed', 'Not Agreed'),
    ], string='Agreed')
    cso_compatible = fields.Selection([
        ('compatible', 'Compatible with scope '),
        ('Incompatible', 'Incompatible with scope '),
    ], string='Compatible')
    company_id = fields.Many2one(string='Company', comodel_name='res.company',
                                 default=lambda self: self.env.user.company_id)
    attachment_booklet_uploade = fields.Binary(string="Upload Booklet")
    # selection" competition/tender_type نوع المنافسة
    # char" document cost اقيمة الوثائق
    document_cost = fields.Char('Document cost')
    # - char" Body Technical name اسم الجهة الفنية
    body_technical = fields.Char('Body Technical')
    # - pre-qualification linked? مربوط بتأهيل مسبق؟ =No , Yes > initial guarantee percentage (%)  نسبة الضمان الابتدائي2- applying address عنوان تقديم الضمان
    pre_qualification = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Pre-Qualification Linked ?')
    initial_guarantee_percentage = fields.Float(
        'Initial Guarantee Percentage (%)')
    applying_address = fields.Char('Applying Address')
    # - alternative offer allowed؟ يسمح بالعرض البديل؟ Yes , No
    alternative_offer_allowed = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Alternative Offer Allowed ?')
    # - is competition divisible? هل المنافسة قابلة للتجزئة؟ No , Yes > Classify توضيح
    is_competition_divisible = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Is Competition Divisible?')
    classify_des = fields.Text('Classify')

    # attachment_commercial = fields.Binary(string="commercial registration")
    # attachment_contractors = fields.Binary(string="contractors classification")
    # attachment_ZAKAT = fields.Binary(string="ZAKAT Certificate")
    # attachment_VAT = fields.Binary(string="VAT Certificate")
    # attachment_insurance = fields.Binary(string="Social Insurance certificate")
    # attachment_commerce = fields.Binary(string="Commerce Participation Certificate")
    # attachment_saudi_cer = fields.Binary(string="Saudi certificate")
    # attachment_investment = fields.Binary(string="Investment license")

    tender_name = fields.Char('Tender Name')
    purpose_of_tender = fields.Char('Purpose of Tender ')
    is_delivered = fields.Selection([
        ('no', 'NO'),
        ('yes', 'YES')
    ], string='Do samples need to delivered')

    samples_delivery_address = fields.Char('Samples  Address')
    delivery_building = fields.Char('building')
    delivery_floor = fields.Char('Floor')
    delivery_unit = fields.Char('Unit')
    date_time = fields.Datetime('Date and Time')
    Delivery_place = fields.Selection([
        ('out', 'Out of Saudi Arabia'),
        ('inside', 'Inside  Saudi Arabia')
    ], string='Delivery_place')
    other_details = fields.Text('Other details')
    activities = fields.Many2many('activity.type', string='Activities')
    project_duration = fields.Char('numbers of project duration')
    activity_description = fields.Text('Activity Description',)
    # other description  تعريف المنافسة
    competion_description = fields.Text('Competion Description')
    # - List of documentaries قائمة الوئاق
    list_documentaries = fields.Text('List documentaries')
    # - Scope of project نطاق عمل المشروع (ارفاق مستند)
    attachment_scope_project = fields.Binary(string="Attachment Scope Project")
    # - Program of action  برنامج العمل
    program_action = fields.Char('Program of action')
    # - work location 3 char fields -District + City + State +GPS موقع العمل: 1- الحي 2- محافظة/مدينة 3- في محافظة 4- احداثيات
    work_location_district = fields.Char('Work Location District')
    work_location_city = fields.Char('Work Location City')
    work_location_state = fields.Char('Work Location State')
    work_location_GPS = fields.Char('Work Location GPS')
# # - How to implement business and service  طريقة تنفيذ الاعمال والخدمات
#     business_service = fields.Html('How to implement business and service', related="company_id.business_service")
# # - quality classification  مواصفات الجودة
#     quality_classification = fields.Html('quality classification' ,related="company_id.quality_classification",)
# # - Security classification  مواصفات السلامة
#     security_classification = fields.Html('Security classification' ,related="company_id.security_classification",)
# # - Special Terms and Conditions الشروط الخاصة
#     special_terms_conditions = fields.Html('Special Terms and Conditions' ,related="company_id.special_terms_conditions",)

    # END INFO Ordinary purchase request

    def download_url(self):
        return {
            "type": "ir.actions.act_url",
            "url": '/web/content/res.company/%s/attachment_booklet_exp/الكراسة الالكترونية الموحدة.docx' % self.company_id.id,
            "target": "new",
        }

    def action_confirm(self):
        super(PurchaseRequest, self).action_confirm()
        if self.purchase_request_type in ['emarket','strategy']:
            amount_total = self.amount_total
            if amount_total < self.company_id.exceptional_amount:
                self.write({'state': 'send_budget'})
            else:
                self.write({'state': 'CSO'})
        else:
            self.write({
                'state': 'ppmo'
            })

    def action_dm_confirm(self):
        super(PurchaseRequest, self).action_dm_confirm()
        if self.purchase_request_type == 'ordinary':
            self.write({
                'state': 'procurement_unit'
            })

    def action_procurement_unit(self):
        self.write({
            'state': 'ppmm'
        })

    def action_ppmm(self):
        self.write({
            'state': 'ppmm'
        })

    def action_CSO(self):
        if self.purchase_request_type == 'ordinary' and self.state == 'ppmm':
            self.write({'state': 'dm1'})
        else:
            amount_total = self.amount_total
            if amount_total < self.company_id.exceptional_amount:
                self.write({'state': 'send_budget'})
            else:
                self.write({'state': 'CSO'})

    # write -m purchase.request -i 56 -v {'state':'procurement'}
    def action_CSO_send(self):
        if self.is_direct_manager:
            self.write({'state': 'direct_manager'})
        else:
            self.write({'state': 'send_budget'})

    def action_direct_manager(self):
        self.write({'state': 'send_budget'})

    def action_chairman_vision_office(self):
        if self.purchase_request_type in ['ordinary','emarket','strategy'] and self.state == 'procurement':
            self.write({'state': 'ceo_purchase'})
        else:
            self.write({'state': 'chairman_vision_office'})

    def action_cs_approve(self):
        self.write({'state': 'ceo_purchase'})

    def action_ceo_purchase(self):
        amount_total = self.amount_total
        if amount_total < self.company_id.direct_purchase:
            self.write({'state': 'waiting'})
        else:
            self.write({'state': 'budget_approve'})

    def action_budget_approve(self):
        amount_total = self.amount_total
        if amount_total < self.company_id.chief_executive_officer:
            self.write({'state': 'waiting'})
        else:
            self.write({'state': 'general_supervisor'})
