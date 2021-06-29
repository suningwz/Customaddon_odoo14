import requests
import json
from datetime import datetime
from odoo import fields, models, api
from urllib.request import urlopen
import base64


class SendoSellerProduct(models.Model):
    _name = "sendo.seller.product"
    _description = "Seller Product Sendo"

    seller_product_id = fields.Char(string='Product ID', store=True)
    category_for_name = fields.Char(string='Category', store=True)
    name = fields.Char(string='Product Name', store=True)
    final_price_min = fields.Float(string='Price', store=True)
    stock_quantity = fields.Integer(string='Available Product', store=True)
    sku = fields.Char('SKU', store=True)
    category_for_id = fields.Integer(store=True)
    store_name = fields.Char(store=True)
    image = fields.Binary(store=True)

    date_from = fields.Char(store=True, default='')
    date_to = fields.Char(store=True, default=(datetime.today()).strftime("%Y-%m-%d"))

    # product_get_token = fields.Many2many('sendo.connect.wizard')
    # token_sendo = fields.Char(related='product_get_token.token_connection')

    # @api.onchange('date_from')
    def get_date_to(self):
        self.date_to = (datetime.today()).strftime("%Y-%m-%d")

        # Function get list product
        self.get_seller_product_sendo()

        self.date_from = self.date_to

    #       Add To Module Sendo Integration
    def get_seller_product_sendo(self):
        try:
            current_seller = self.env['sendo.seller'].sudo().search([])[0]

            url = "https://open.sendo.vn/api/partner/product/search/"

            payload = json.dumps({
                "page_size": 10,
                "product_name": "",
                "date_from": self.date_from or None,
                "date_to": self.date_to or None
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
                    val['category_for_name'] = product['category_4_name']
                    val['name'] = product['name']
                    val['final_price_min'] = product['final_price_min']
                    val['stock_quantity'] = product['stock_quantity']
                    val['sku'] = product['sku']
                    val['category_for_id'] = product['cate_4_id']
                    val['store_name'] = product['store_name']
                    val['image'] = base64.b64encode(urlopen(product["image"]).read())
                    existed_seller_product = self.env['sendo.seller.product'].search(
                        [('seller_product_id', '=', product['id'])], limit=1)
                    if len(existed_seller_product) < 1:
                        self.env['sendo.seller.product'].create(val)
                    else:
                        existed_seller_product.write(val)

        except Exception as e:
            print(e)

    #       Add To Module Sale
    def get_product_sendo_to_product_template(self):
        try:
            current_seller = self.env['sendo.seller'].sudo().search([])[0]

            url = "https://open.sendo.vn/api/partner/product/search/"

            payload = json.dumps({
                "page_size": 10,
                "product_name": "",
                "date_from": self.date_from or None,
                "date_to": self.date_to or None
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
                    val['type'] = 'product'
                    val['categ_id'] = 1
                    val['name'] = product['name']
                    val['list_price'] = product['final_price_min']
                    # val['qty_available'] = product['stock_quantity']
                    val['default_code'] = product['sku']
                    # val['category_for_id'] = product['cate_4_id']
                    # val['store_name'] = product['store_name']
                    val['sale_ok'] = True
                    val['purchase_ok'] = False
                    val['image_1920'] = base64.b64encode(urlopen(product["image"]).read())
                    existed_seller_product = self.env['product.template'].search([('name', '=', product['name'])], limit=1)
                    if len(existed_seller_product) < 1:
                        self.env['product.template'].create(val)
                    else:
                        existed_seller_product.write(val)

        except Exception as e:
            print(e)
