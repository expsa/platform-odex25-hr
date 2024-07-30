# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website


class ZuhairFayezHomwPage(Website):
    @http.route('/', type='http', auth='public', website=True)
    def index(self, **kw):
        web_years = request.website.no_of_years
        web_video = request.website.video_bg
        print('vy = ', web_years)
        print('vv = ', web_video)
        return http.request.render("zuhair_fayez_website.show_website_info", {'years': web_years, "link": web_video})

class ZuhairFayez(http.Controller):

    @http.route('/services', type='http', auth='public', website=True)
    def services(self, **kw):
        services = http.request.env['website.project.service'].sudo().search([('is_main', '=', True)])
        return http.request.render('zuhair_fayez_website.services', {'services': services})

    @http.route('/contact', type='http', auth='public', website=True)
    def contact(self, **kw):
        return http.request.render("zuhair_fayez_website.contact")

    @http.route('/news', type='http', auth='public', website=True)
    def news(self, **kw):
        news = http.request.env['website.media'].sudo().search([],limit=6)
        vals = {'news':news}
        return http.request.render("zuhair_fayez_website.news",vals)

    @http.route('/activites', type='http', auth='public', website=True)
    def activites(self, **kw):
        return http.request.render("zuhair_fayez_website.activites")

    @http.route('/awards', type='http', auth='public', website=True)
    def awards(self, **kw):
        return http.request.render("zuhair_fayez_website.awards")

    @http.route('/news_details', type='http', auth='public', website=True)
    def news_details(self, **kw):
        return http.request.render("zuhair_fayez_website.news_details")

    @http.route('/careers', type='http', auth='public', website=True)
    def careers(self, **kw):
        return http.request.render("zuhair_fayez_website.careers")

    @http.route('/job_details', type='http', auth='public', website=True)
    def job_details(self, **kw):
        return http.request.render("zuhair_fayez_website.job_details")

    @http.route('/service_sub_projects', type='http', auth='public', website=True)
    def service_sub_projects(self, **kw):
        id = kw.get('id')
        print(id)
        projects = http.request.env['project.project'].sudo().search([('service_id','=',int(id))])
        vals = {'projects': projects}
        return http.request.render("zuhair_fayez_website.service_sub_projects",vals)

    @http.route('/project_details', type='http', auth='public', website=True)
    def project_details(self, **kw):
        return http.request.render("zuhair_fayez_website.project_details")

    @http.route('/service', type='http', auth='public', website=True)
    def service(self, **kw):
        id = kw.get('id')
        print(id)
        main_service = http.request.env['website.project.service'].sudo().search([('is_main', '=', True),('id', '=', id),])
        sub_service = main_service.child_ids
        vals = {'sub_service': sub_service}
        print('testtt del', sub_service)
        return http.request.render("zuhair_fayez_website.service",vals)

    @http.route('/about', type='http', auth='public', website=True)
    def about(self, **kw):
        return http.request.render("zuhair_fayez_website.about")
