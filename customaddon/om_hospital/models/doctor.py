# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"
    # _rec_name = "reference"

    name = fields.Char(string='Name', required=True, tracking=True)
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    age = fields.Integer(string='Age', tracking=True, copy=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    image = fields.Binary(string='Patient Image')

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.doctor') or _('New')
        res = super(HospitalDoctor, self).create(vals)
        return res

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (Copy)", self.name)
        # default['note'] = ''
        return super(HospitalDoctor, self).copy(default)

