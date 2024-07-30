# controllers/main.py
import json
import logging
import werkzeug.utils

from odoo import http
from odoo.http import request
from odoo.osv.expression import AND
from odoo.addons.point_of_sale.controllers.main import PosController

_logger = logging.getLogger(__name__)
CONFIG_PARAM_WEB_WINDOW_TITLE = "web.base.title"


class CustomPosController(PosController):

    @http.route(['/pos/web', '/pos/ui'], type='http', auth='user')
    def pos_web(self, config_id=False, **k):
        res = super(CustomPosController, self).pos_web(config_id=config_id, **k)

        web_window_title = request.env['ir.config_parameter'].sudo().get_param(CONFIG_PARAM_WEB_WINDOW_TITLE, 'Odoo Jan')
        _logger.info("Fetched web_window_title in controller: %s", web_window_title)

        context = res.qcontext if hasattr(res, 'qcontext') else {}
        context.update({'web_window_title': web_window_title})

        res.qcontext = context
        return res
