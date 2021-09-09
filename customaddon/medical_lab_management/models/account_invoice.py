
from odoo import models, fields, api


class LabRequestInvoices(models.Model):
    _inherit = 'account.move'

    is_lab_invoice = fields.Boolean(string="Is Lab Invoice")
    lab_request = fields.Many2one('lab.appointment', string="Lab Appointment", help="Source Document")

    def action_invoice_paid(self):
        res = super(LabRequestInvoices, self).action_invoice_paid()
        lab_app_obj = self.env['lab.appointment'].search([('id', '=', self.lab_request.id)])
        for obj in lab_app_obj:
            obj.write({'state': 'invoiced'})
        return res
