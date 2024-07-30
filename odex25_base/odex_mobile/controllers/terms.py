from odoo import http
from odoo.http import request


class TermsController(http.Controller):
    @http.route(
        "/rest_api/web/odexss/terms",
        type="http",
        auth="none",
        csrf=False,
        cors="*",
        methods=["GET"],
    )
    def terms_of_user(self, **kw):
        return http.request.render("odex_mobile.terms_of_use", {})

    @http.route(
        "/rest_api/web/odexss/privacy",
        type="http",
        auth="none",
        csrf=False,
        cors="*",
        methods=["GET"],
    )
    def privacy_policy(self, **kw):
        return http.request.render("odex_mobile.privacy_policy", {})
