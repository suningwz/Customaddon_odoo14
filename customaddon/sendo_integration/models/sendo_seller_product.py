import requests
import json
from datetime import datetime
from odoo import fields, models, api
from urllib.request import urlopen
import base64


class SendoSellerProduct(models.Model):
    _name = "sendo.seller.product"
    _description = "Seller Product"

    seller_product_id = fields.Char(string='Product ID')
    category_for_name = fields.Char(string='Category')
    name = fields.Char(string='Product Name')
    promotion_price = fields.Float(string='Price')
    stock_quantity = fields.Integer(string='Available Product')
    sku = fields.Char('SKU')
    category_for_id = fields.Integer()
    store_name = fields.Char()
    image = fields.Binary()

    date_from = fields.Char()
    date_to = fields.Char()

    # product_get_token = fields.Many2many('sendo.connect.wizard')
    # token_sendo = fields.Char(related='product_get_token.token_connection')

    @api.onchange('date_from')
    def get_date_to(self):
        for rec in self:
            rec.date_to = (datetime.today()).strftime("%Y-%m-%d")

            # Function get list product
            rec.get_seller_product_sendo()

            rec.date_from = rec.date_to

    def get_seller_product_sendo(self):
        for rec in self:
            current_seller = self.env['sendo.seller'].sudo().search([])[0]

            url = "https://open.sendo.vn/api/partner/product/search/"

            payload = json.dumps({
                "page_size": 10,
                "product_name": "",
                "date_from": rec.date_from,
                "date_to": rec.date_to
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + current_seller.token_connection
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            seller_products = response.json()
            list_products = seller_products["result"]["data"]

            val = {}
            for product in list_products:
                if 'id' in product:
                    val['seller_product_id'] = product['id']
                    val['category_4_name'] = product['category_4_name']
                    val['name'] = product['name']
                    val['final_price_min'] = product['final_price_min']
                    val['stock_quantity'] = product['stock_quantity']
                    val['sku'] = product['sku']
                    val['category_for_id'] = product['category_for_id']
                    val['store_name'] = product['store_name']
                    val['image'] = base64.b64encode(urlopen(product["image"]).read())
                self.env['sendo.seller.product'].create(val)
