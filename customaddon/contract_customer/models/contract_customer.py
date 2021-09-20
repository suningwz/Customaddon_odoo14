from odoo import _, models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date


class ContractCustomer(models.Model):
    _name = 'contract.customer'
    _rec_name = "contract_id"

    contract_id = fields.Char()
    customer_name = fields.Char()
    signing_date = fields.Date(default=date.today())
    amount_total = fields.Float()
    state = fields.Selection([('new', "Mới"),
                              ('done', "Hoàn thành")], default="new")

    contract_sale_order = fields.One2many("sale.order", "sale_order_contract_id", string="Information Order")

    def action_done(self):
        self.state = 'done'
