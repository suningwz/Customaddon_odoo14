from odoo import fields, models, api


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    # product_in_list_order_sale_order = fields.Many2one('sale.order')

