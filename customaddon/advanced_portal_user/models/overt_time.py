# -*- coding: utf-8 -*-
from datetime import date

from odoo import models, fields, api, _


class OverTime(models.Model):
    _name = 'hr.over.time'
    _description = 'New model for sign over time'

    user_id = fields.Many2one('res.users')
    employee_id = fields.Many2one('hr.employee')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('refused', 'Refused')], 'Status', default="draft")
    description = fields.Text('Description')
    approver = fields.Many2one('res.users', string='Approver', compute='_get_user', store=True)
    user_is_approver = fields.Boolean(default=False, compute='_check_user_is_approver')
    time_from = fields.Datetime(string='Time From')
    time_to = fields.Datetime(string='Time To')

    def _get_user(self):
        self.approver = self.env.user.id
        return self.approver
    ###
    # assign approver for person who create record
    ###

    def _check_user_is_approver(self):
        for rec in self:
            if rec.env.user.id == rec.approver.id:
                rec.user_is_approver = True
            else:
                rec.user_is_approver = False
    ###
    # check permission for display and approver request over time
    ###

    def approved_action(self):
        self.state = 'approved'
        message = _(
            "%(approver_name)s approved the overtime request of %(employee_name).",
            approver_name=self.approver.login,
            employee_name=self.employee_id.name
        )
        self.message_post(body=message, subject='Over Time Approving',
                          approved_ids=self.user_id.id)

    def refused_action(self):
        self.state = 'refused'
        message = _(
            "%(approver_name)s refused the overtime request of %(employee_name).",
            approver_name=self.approver.login,
            employee_name=self.employee_id.name
        )
        self.message_post(body=message, subject='Over Time Approving',
                          approved_ids=self.user_id.id)
