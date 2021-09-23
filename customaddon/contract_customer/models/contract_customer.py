from odoo import _, models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date


class ContractCustomer(models.Model):
    _name = 'contract.customer'
    _rec_name = "contract_id"

    contract_id = fields.Char(string='Contract Reference', required=True, copy=False, readonly=True,
                              default=lambda self: _('New'))
    signing_date = fields.Date(default=date.today())
    amount_total = fields.Float()
    state = fields.Selection([('new', "Mới"),
                              ('done', "Hoàn thành")], default="new")

    customer_name_id = fields.Many2one('res.partner', string='Customer Name')
    contract_sale_order = fields.One2many("sale.order", "sale_order_contract_id", string="Information Order")
    payments_contract_id = fields.One2many('contract.payments', 'contract_payment_customer', string='Payments Contract')

    @api.onchange('payments_contract_id')
    def check_onchange_payments_contract_id(self):
        if self.payments_contract_id:
            total_percent = 0
            list_percent = self.payments_contract_id.mapped('percent_payment')
            for percent in list_percent:
                if percent:
                    total_percent += percent
            if total_percent > 100:
                raise ValidationError('Total Percent Payment Value must be equal to 100')

    def action_done(self):
        self.state = 'done'

    @api.model
    def create(self, vals):
        if vals.get('contract_id', _('New')) == _('New'):
            vals['contract_id'] = self.env['ir.sequence'].next_by_code('contract.customer') or _('New')
        res = super(ContractCustomer, self).create(vals)
        print(res.id)
        return res


class ContractPayments(models.Model):
    _name = "contract.payments"
    _description = "Contract Payments"

    percent_payment = fields.Float(string='Percent Payments (%)')
    total_amount = fields.Float(compute='_compute_calculate_money')
    date_payment = fields.Date(default=date.today())

    contract_payment_customer = fields.Many2one('contract.customer', string="Appointment")

    @api.depends('percent_payment')
    def _compute_calculate_money(self):
        check_percent = 0
        for rec in self:
            if rec.percent_payment > 100:
                raise ValidationError('Percent Payment Value must be smaller than 100')
            elif rec.percent_payment < 0:
                raise ValidationError('Percent Payment Value must be greater than 0')
            else:
                check_percent = check_percent + rec.percent_payment
                if check_percent <= 100:
                    rec.total_amount = rec.percent_payment / 100 * self.contract_payment_customer.amount_total
                else:
                    raise ValidationError('Total Percent Payment Value must be equal to 100')



