from odoo import fields, models, api


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    money_debt = fields.Float(string='Hạn mức tiền nợ')
    time_debt = fields.Float(string='Hạn mức thời gian nợ (Tháng)')

    def check_debt_customer(self):
        money_debit = 0
        for order in self.sale_order_ids:
            if order.state == 'draft':
                money_debit = money_debit + order.amount_total
            else:
                pass
        return money_debit
