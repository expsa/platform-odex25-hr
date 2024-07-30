# -*- coding: utf-8 -*-

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    odex25_helpdesk_target_closed = fields.Float(string='Target Tickets to Close', default=1)
    odex25_helpdesk_target_rating = fields.Float(string='Target Customer Rating', default=100)
    odex25_helpdesk_target_success = fields.Float(string='Target Success Rate', default=100)

    _sql_constraints = [
        ('target_closed_not_zero', 'CHECK(odex25_helpdesk_target_closed > 0)', 'You cannot have negative targets'),
        ('target_rating_not_zero', 'CHECK(odex25_helpdesk_target_rating > 0)', 'You cannot have negative targets'),
        ('target_success_not_zero', 'CHECK(odex25_helpdesk_target_success > 0)', 'You cannot have negative targets'),
    ]

    def __init__(self, pool, cr):
        """ Override of __init__ to add access rights.
            Access rights are disabled by default, but allowed
            on some specific fields defined in self.SELF_{READ/WRITE}ABLE_FIELDS.
        """
        init_res = super(ResUsers, self).__init__(pool, cr)
        odex25_helpdesk_fields = [
            'odex25_helpdesk_target_closed',
            'odex25_helpdesk_target_rating',
            'odex25_helpdesk_target_success',
        ]
        # duplicate list to avoid modifying the original reference
        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(odex25_helpdesk_fields)
        # duplicate list to avoid modifying the original reference
        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend(odex25_helpdesk_fields)
        return init_res
