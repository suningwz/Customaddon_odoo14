import requests
import json
from datetime import datetime
from odoo import fields, models, api


class SendoListOrder(models.Model):
    _name = "sendo.list.order"
    _description = "List Order Sendo"

    #       Add To Module Sale
    def get_list_order_sendo_to_product_template(self):
        current_seller = self.env['sendo.seller'].sudo().search([])[0]

        url = "https://open.sendo.vn/api/partner/salesorder/search"
        payload = json.dumps({
            "page_size": 50,
            "order_status": None,
            "order_date_from": "2021-06-18",
            "order_date_to": "2021-06-25",
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
        list_order = seller_products["result"]["data"]

        val = {}
        list_product = []
        val_customer = {}
        for rec in list_order:
            if 'sales_order' in rec:
                val_order = rec['sales_order']

                #   Get Information Customer
                val_customer['name'] = val_order['receiver_name']
                val_customer['phone'] = val_order['buyer_phone']
                val_customer['mobile'] = str(val_order['buyer_phone'])
                val_customer['email'] = val_order['receiver_email']
                val_customer['company_type'] = 'person'
                val_customer['type'] = 'contact'
                val_customer['street'] = val_order['receiver_full_address']
                val_customer['comment'] = 'Sync By Call Sendo API'

                #   Check Customer
                existed_customer = self.env['res.partner'].sudo().search(
                    ['&', ('phone', '=', str(val_order['buyer_phone'])),
                     ('street', '=', val_order['receiver_full_address'])], limit=1)
                if len(existed_customer) < 1:
                    self.env['res.partner'].create(val_customer)
                    get_customer = self.env['res.partner'].sudo().search(
                        ['&', ('phone', '=', str(val_order['buyer_phone'])),
                         ('street', '=', val_order['receiver_full_address'])], limit=1)

                    # Get Information Order
                    val['sendo_order_number'] = str(val_order['order_number'])
                    val['sendo_order_status'] = str(val_order['order_status'])
                    val['sendo_payment_status'] = str(val_order['payment_status'])
                    val['sendo_payment_method'] = str(val_order['payment_method'])
                    val['amount_total'] = val_order['total_amount']
                    val['amount_untaxed'] = val_order['sub_total']
                    val['date_order'] = datetime.fromtimestamp(val_order['order_date_time_stamp'])
                    val['partner_id'] = get_customer.id

                    #   Check Order In Database
                    existed_order = self.env['sale.order'].sudo().search(
                        [('sendo_order_number', '=', str(val_order['order_number']))], limit=1)
                    if len(existed_order) < 1:
                        new_record = self.env['sale.order'].create(val)
                        if new_record:
                            if 'sku_details' in rec:
                                val_product = rec['sku_details']
                                for product in val_product:
                                    existed_product_sendo = self.env['product.template'].sudo().search(
                                        [('default_code', '=', product['sku'])], limit=1)
                                    list_product.append({
                                        'product_id': existed_product_sendo.product_variant_id.id,
                                        'product_uom_qty': product['quantity'],
                                        'price_unit': product['price']
                                    })
                                    if list_product:
                                        new_record.order_line = [(0, 0, e) for e in list_product]
                                    list_product = []
                    else:
                        existed_order.sudo().write(val)
                else:
                    # Get Information Order
                    val['sendo_order_number'] = str(val_order['order_number'])
                    val['name'] = str(val_order['order_number'])
                    val['sendo_order_status'] = str(val_order['order_status'])
                    val['sendo_payment_status'] = str(val_order['payment_status'])
                    val['sendo_payment_method'] = str(val_order['payment_method'])
                    val['amount_total'] = val_order['total_amount']
                    val['amount_untaxed'] = val_order['sub_total']
                    val['date_order'] = datetime.fromtimestamp(val_order['order_date_time_stamp'])
                    val['partner_id'] = existed_customer.id
                    #   Check Order In Database
                    existed_order = self.env['sale.order'].sudo().search(
                        [('sendo_order_number', '=', str(val_order['order_number']))], limit=1)
                    if len(existed_order) < 1:
                        new_record = self.env['sale.order'].create(val)
                        if new_record:
                            if 'sku_details' in rec:
                                val_product = rec['sku_details']
                                for product in val_product:
                                    existed_product_sendo = self.env['product.template'].sudo().search(
                                        [('default_code', '=', product['sku'])], limit=1)
                                    list_product.append({
                                        'product_id': existed_product_sendo.product_variant_id.id,
                                        'product_uom_qty': product['quantity'],
                                        'price_unit': product['price']
                                    })
                                    if list_product:
                                        new_record.order_line = [(0, 0, e) for e in list_product]
                                    list_product = []
                    else:
                        existed_order.sudo().write(val)
                    pass


