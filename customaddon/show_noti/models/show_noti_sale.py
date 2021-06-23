from odoo import models, fields, api
from datetime import *
from odoo.exceptions import UserError, ValidationError


class NeedActionMixinInherit(models.Model):
    _name = 'need.action.mixin.inherit'
    _inherit = ['ir.needaction_mixin', 'purchase.order']

    @api.model
    def _needaction_domain_get(self):
        return False

    @api.model
    def _needaction_count(self, domain=None):
        return self.search_count(domain)
