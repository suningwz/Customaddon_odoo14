import requests
import json
from datetime import datetime
from odoo import fields, models, api


class SendoListOrder(models.Model):
    _name = "sendo.list.order"
    _description = "List Order Sendo"
    _rec_name = 'order_number'

    #   Information Order
    order_number = fields.Char()
    order_status = fields.Selection([
        ('2', 'Mới'),
        ('3', 'Đang xử lý'),
        ('6', 'Đang vận chuyển'),
        ('7', 'Đã giao hàng'),
        ('8', 'Đã hoàn tất'),
        ('10', 'Đóng'),
        ('11', 'Yêu cầu hoãn'),
        ('12', 'Đang hoãn'),
        ('13', 'Hủy'),
        ('14', 'Yêu cầu tách'),
        ('15', 'Chờ tách'),
        ('19', 'Chờ gộp'),
        ('21', 'Đang đổi trả'),
        ('22', 'Đổi trả thành công'),
        ('23', 'Chờ Sendo xử lý')], string='Order Status')
    payment_status = fields.Selection([
        ('1', 'Chưa thanh toán'),
        ('2', 'Đã thanh toán COD'),
        ('3', 'Đã thanh toán'),
        ('4', 'Hoàn tất'),
        ('5', 'Đã hoàn tiền'),
        ('6', 'Đợi xác nhận'),
        ('7', 'Từ chối'),
        ('14', 'Đã thanh toán một phần'),
        ('15', 'Đã hoàn tiền một phần')], string='Payment Status')
    payment_method = fields.Selection([
        ('1', 'Thanh toán khi nhận hàng'),
        ('2', 'Thanh toán trực tuyến'),
        ('4', 'Thanh toán kết hợp'),
        ('5', 'Thanh toán trả sau')], string='Payment Method')
    total_amount = fields.Float()
    total_amount_buyer = fields.Float()
    sub_total = fields.Float()
    receiver_name = fields.Char()
    buyer_phone = fields.Integer()
    receiver_full_address = fields.Char()
    receiver_email = fields.Char()

    #   Information Product In Order
    # product_variant_id = fields.Integer(string='Product ID')
    # product_name = fields.Char(string='Product')
    # sku = fields.Char(string='SKU')
    # quantity = fields.Integer()
    # price = fields.Float()

    date_from = fields.Char()
    date_to = fields.Char()

    # order_get_token = fields.Many2many('sendo.connect.wizard')
    # token_sendo = fields.Char(related='order_get_token.token_connection')

    product_in_order = fields.One2many('product.order.sendo', 'product_in_list_order', string='Information Product')

    @api.onchange('date_from')
    def get_date_to(self):
        self.date_to = (datetime.today()).strftime("%Y-%m-%d")

        # Function get list product
        self.get_list_order_sendo()

        self.date_from = self.date_to

    def get_list_order_sendo(self):
        current_seller = self.env['sendo.seller'].sudo().search([])[0]

        url = "https://open.sendo.vn/api/partner/salesorder/search"
        payload = json.dumps({
            "page_size": 10,
            "order_status": None,
            "order_date_from": self.date_from or None,
            "order_date_to": self.date_to or None,
            "order_status_date_from": None,
            "order_status_date_to": None,
            "token": None
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + current_seller.token_connection
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        seller_products = response.json()
        # list_order = seller_products["result"]["data"]
        # print(list_order)
        # # ["sales_order"]
        # detail_order = seller_products["result"]["data"]["sku_details"]
        list_order = seller_products["result"]["data"]

        val = {}
        list_product = []
        for rec in list_order:
            if 'sales_order' in rec:
                val_order = rec['sales_order']
                val['order_number'] = str(val_order['order_number'])
                val['order_status'] = str(val_order['order_status'])
                val['payment_status'] = str(val_order['payment_status'])
                val['payment_method'] = str(val_order['payment_method'])
                val['total_amount'] = val_order['total_amount']
                val['total_amount_buyer'] = val_order['total_amount_buyer']
                val['sub_total'] = val_order['sub_total']
                val['receiver_name'] = val_order['receiver_name']
                val['buyer_phone'] = val_order['buyer_phone']
                val['receiver_full_address'] = val_order['receiver_full_address']
                val['receiver_email'] = val_order['receiver_email']
                existed_order = self.env['sendo.list.order'].search([('order_number', '=', str(val_order['order_number']))], limit=1)
                if len(existed_order) < 1:
                    new_record = self.env['sendo.list.order'].create(val)
                    if new_record:
                        if 'sku_details' in rec:
                            val_product = rec['sku_details']
                            for product in val_product:
                                list_product.append({
                                    'product_variant_id': str(product['product_variant_id']),
                                    'product_name': product['product_name'],
                                    'sku': product['sku'],
                                    'quantity': product['quantity'],
                                    'price': product['price']
                                })
                                if list_product:
                                    new_record.product_in_order = [(0, 0, e) for e in list_product]
                else:
                    existed_order.env['sendo.list.order'].sudo().write(val)
                    # pass


# val_order = {}
# for order in list_order:
#     val_order['order_number'] = order['order_number']
#     val_order['order_status'] = order['order_status']
#     val_order['payment_status'] = order['payment_status']
#     val_order['payment_method'] = order['payment_method']
#     val_order['total_amount'] = order['total_amount']
#     val_order['total_amount_buyer'] = order['total_amount_buyer']
#     val_order['sub_total'] = order['sub_total']
#     val_order['receiver_name'] = order['receiver_name']
#     val_order['buyer_phone'] = order['buyer_phone']
#     val_order['receiver_full_address'] = order['receiver_full_address']
#     val_order['receiver_email'] = order['receiver_email']
#     self.env['sendo.list.order'].create(val_order)
#
# val_product = {}
# for product in detail_order:
#     val_product['product_variant_id'] = product['product_variant_id']
#     val_product['product_name'] = product['product_name']
#     val_product['sku'] = product['sku']
#     val_product['quantity'] = product['quantity']
#     val_product['price'] = product['price']
# self.env['sendo.list.order'].create(val_product)


class ProductOrderSendo(models.Model):
    _name = "product.order.sendo"
    _description = "Appointment Prescription Line"

    #   Information Product In Order
    product_variant_id = fields.Char(string='Product ID')
    product_name = fields.Char(string='Product')
    sku = fields.Char(string='SKU')
    quantity = fields.Integer()
    price = fields.Float()

    product_in_list_order = fields.Many2one('sendo.list.order', string="Appointment")
