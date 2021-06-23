# -*- coding: utf-8 -*-
import datetime
from odoo import api, models, _
from odoo.tools.safe_eval import safe_eval


#
# Use period and Journal for selection or resources
#


class ir_needaction_mixin(models.AbstractModel):
    _name = 'ir.needaction_mixin'
    _needaction = True

    # ------------------------------------------------------
    # Addons API
    # ------------------------------------------------------

    def _needaction_domain_get(self, cr, uid, context=None):
        """ Returns the domain to filter records that require an action
            :return: domain or False is no action
        """
        return False

    # ------------------------------------------------------
    # "Need action" API
    # ------------------------------------------------------

    def _needaction_count(self, cr, uid, domain=None, context=None):
        """ Get the number of actions uid has to perform. """
        dom = self._needaction_domain_get(cr, uid, context=context)
        if not dom:
            return 0
        res = self.search(cr, uid, (domain or []) + dom, limit=100, order='id DESC', context=context)
        return len(res)
