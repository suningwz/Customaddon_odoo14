# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"

    name = fields.Char(string='Name', required=True, tracking=True)
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string='Status', defaul='draft', tracking=True)
    responsible_id = fields.Many2one('res.partner', string='Responsible')
    appointment_count = fields.Integer(compute='_compute_appointment_count')
    image = fields.Binary(string='Patient Image')
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointment')

    def _compute_appointment_count(self):
        for rec in self:
            temp_count = rec.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = temp_count

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Patient'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        res = super(HospitalPatient, self).create(vals)
        return res

    @api.model
    def default_get(self, fields):
        res = super(HospitalPatient, self).default_get(fields)
        # if not res.get['gender']:
        # res['gender'] = 'other'
        res['state'] = 'draft'
        res['note'] = 'Test override'
        return res

    @api.constrains('name')
    def check_name(self):
        for rec in self:
            patients = rec.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError(_('Name "%s" Already Exists' % rec.name))

    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age <= 0:
                raise ValidationError(_("Age need more than 0."))

    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = '[' + record.reference + ']' + ' ' + record.name
    #         result.append((record.id, name))
    #     return result