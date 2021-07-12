from odoo import fields, models, api, _


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    chech_sendo_customer = fields.Boolean()