# -*- coding: utf-8 -*-
from datetime import date

from odoo import models, fields, api


class AdvancedPortal(models.Model):
    _inherit = 'res.users'
    _description = 'Add check Portal User'

    portal_employee = fields.Boolean(default=False)

    # employee_id = fields.Many2one(string='Employee', comodel_name='hr.employee')

    @api.model
    def create(self, vals):
        res = super(AdvancedPortal, self).create(vals)
        if res.portal_employee:
            res.env['hr.employee'].sudo().create({
                'name': res.name,
                'user_id': res.id,
            })
            # set leave_manage_id to manage leave request
            # set parent_id to assign manager
        return res


class UserEmployeeAttendance(models.Model):
    _inherit = 'hr.attendance'

    user_id = fields.Many2one(string='User', comodel_name='res.users')
