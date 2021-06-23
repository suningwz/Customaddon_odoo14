import requests
import json
from datetime import *
from odoo import fields, models, api


class SendoListOrder(models.Model):
    _name = "sendo.list.order"
    _description = "List Order"

    #   Information Order
    order_number = fields.Char()
    order_status = fields.Integer()
    payment_status = fields.Integer()
    payment_method = fields.Integer()
    total_amount = fields.Float()
    total_amount_buyer = fields.Float()
    sub_total = fields.Float()
    receiver_name = fields.Char()
    buyer_phone = fields.Char()
    receiver_full_address = fields.Char()
    receiver_email = fields.Char()

    #   Information Product In Order
    product_variant_id = fields.Char()
    product_name = fields.Char()
    sku = fields.Char()
    quantity = fields.Integer()
    price = fields.Float()

    date_from = fields.Date()
    date_to = fields.Date()

    order_get_token = fields.Many2many('sendo.connect.wizard')
    token_sendo = fields.Char(related='order_get_token.token_connection')

    @api.onchange('date_from')
    def get_date_to(self):
        for rec in self:
            rec.date_to = date.today()

            # Function get list product
            rec.get_list_order_sendo()

            rec.date_from = rec.date_to

    def get_list_order_sendo(self):
        for rec in self:

            url = "https://open.sendo.vn/api/partner/salesorder/search"
            payload = json.dumps({
                "page_size": 10,
                "order_status": None,
                "order_date_from": rec.date_from,
                "order_date_to": rec.date_to,
                "order_status_date_from": None,
                "order_status_date_to": None,
                "token": None
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + rec.token_sendo
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            seller_products = response.json()
            list_order = seller_products["result"]["data"]

            val = {}
            for order in list_order:
                val['order_number'] = order["sales_order"]['order_number']
                val['order_status'] = order["sales_order"]['order_status']
                val['payment_status'] = order["sales_order"]['payment_status']
                val['payment_method'] = order["sales_order"]['payment_method']
                val['total_amount'] = order["sales_order"]['total_amount']
                val['total_amount_buyer'] = order["sales_order"]['total_amount_buyer']
                val['sub_total'] = order["sales_order"]['sub_total']
                val['receiver_name'] = order["sales_order"]['receiver_name']
                val['buyer_phone'] = order["sales_order"]['buyer_phone']
                val['receiver_full_address'] = order["sales_order"]['receiver_full_address']
                val['receiver_email'] = order["sales_order"]['receiver_email']
                for product in list_order:
                    val['product_variant_id'] = product["sku_details"]['product_variant_id']
                    val['product_name'] = product["sku_details"]['product_name']
                    val['sku'] = product["sku_details"]['sku']
                    val['quantity'] = product["sku_details"]['quantity']
                    val['price'] = product["sku_details"]['price']
            self.env['sendo.list.order'].create(val)