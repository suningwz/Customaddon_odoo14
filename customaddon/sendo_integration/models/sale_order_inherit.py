from odoo import fields, models, api


#       Class Inherit Sale Order
class ApiSendoSaleOrderInherit(models.Model):
    _inherit = "sale.order"

    product_in_order_sale_order = fields.One2many('product.order.sendo', 'product_in_list_order_sale_order')
