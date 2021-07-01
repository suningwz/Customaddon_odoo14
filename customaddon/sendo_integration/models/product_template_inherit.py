from odoo import fields, models, api, _
import requests
import json
from odoo.exceptions import UserError, ValidationError
from datetime import *


class ProductTemplateInheritSendo(models.Model):
    _inherit = "product.template"

    sendo_product_id = fields.Char()
    sendo_stock_availability = fields.Boolean(string='Stock Availability', compute='_compute_check_quantity_product')
    sendo_height = fields.Float(string='Height', required=True, default=5)
    sendo_length = fields.Float(string='Length', required=True, default=20)
    sendo_width = fields.Float(string='Width', required=True, default=10)
    sendo_unit_id = fields.Selection([
        ('1', 'Cái'),
        ('2', 'Bộ'),
        ('3', 'Chiếc'),
        ('4', 'Đôi'),
        ('5', 'Hộp'),
        ('6', 'Cuốn'),
        ('7', 'Chai'),
        ('8', 'Thùng')], string='Unit Product', required=True, default='1')
    sendo_stock_quantity = fields.Integer(string='Stock Quantity', required=True, default=50)
    sendo_promotion_from_date = fields.Date(string='Promotion From Date', required=True, default=date.today())
    sendo_promotion_to_date = fields.Date(string='Promotion To Date', required=True, default=date.today() + timedelta(days=9000))
    sendo_is_promotion = fields.Boolean(string='Promotion', compute='_compute_check_promotion_product')
    sendo_special_price = fields.Float(string='Special Price', required=True, default=1)

    @api.constrains('sendo_height')
    def check_sendo_height(self):
        for rec in self:
            if rec.sendo_height <= 0:
                raise ValidationError(_("Height Product need more than 0."))

    @api.constrains('sendo_length')
    def check_sendo_length(self):
        for rec in self:
            if rec.sendo_length <= 0:
                raise ValidationError(_("Length Product need more than 0."))

    @api.constrains('sendo_width')
    def check_sendo_width(self):
        for rec in self:
            if rec.sendo_width <= 0:
                raise ValidationError(_("Width Product need more than 0."))

    @api.constrains('sendo_stock_quantity')
    def check_sendo_stock_quantity(self):
        for rec in self:
            if rec.sendo_stock_quantity < 0:
                raise ValidationError(_("Stock Quantity Product need more than 0."))

    def _compute_check_quantity_product(self):
        for rec in self:
            if rec.sendo_stock_quantity > 0:
                rec.sendo_stock_availability = True
            else:
                rec.sendo_stock_availability = False

    def _compute_check_promotion_product(self):
        for rec in self:
            if rec.sendo_stock_quantity > 0:
                rec.sendo_is_promotion = True
            else:
                rec.sendo_is_promotion = False
    @api.model
    def create(self, vals_list):
        print()
        res = super(ProductTemplateInheritSendo, self).create(vals_list)
        # Call API Create Or Update Product In Sendo
        self.create_or_update_product_sendo()
        return res

    def create_or_update_product_sendo(self):
        current_seller = self.env['sendo.seller'].sudo().search([])[0]

        url = "https://open.sendo.vn/api/partner/product"

        payload = json.dumps({
            "id": 0 or int(self.sendo_product_id),
            "name": self.name,
            "sku": self.default_code,
            "price": self.list_price,
            "weight": self.weight,
            "stock_availability": self.sendo_stock_availability or True,
            "description": self.description,
            "cat_4_id": self.categ_id,
            "tags": None,
            "relateds": [
                {
                    "id": 0,
                    "name": None,
                    "sku": None,
                    "category_name": None,
                    "price": 0,
                    "status": 0,
                    "image": None
                }
            ],
            "seo_keyword": None,
            "seo_title": None,
            "seo_description": None,
            "product_image": self.image_1920,
            "brand_id": None,
            "video_links": None,
            "height": self.sendo_height,
            "length": self.sendo_length,
            "width": self.sendo_width,
            "unit_id": int(self.sendo_unit_id),
            "stock_quantity": self.sendo_stock_quantity,
            "avatar": {
                "picture_url": self.image_1920
            },
            "pictures": [
                {
                    "picture_url": self.image_1920
                }
            ],
            "certificate_file": [
                {
                    "id": 0,
                    "table_name": None,
                    "table_id": 0,
                    "file_name": None,
                    "attachment_url": None,
                    "display_order": 0
                }
            ],
            "attributes": [
                {
                    "attribute_id": 0,
                    "attribute_name": None,
                    "attribute_code": None,
                    "attribute_is_custom": False,
                    "attribute_is_checkout": False,
                    "attribute_values": [
                        {
                            "id": 0,
                            "value": None,
                            "attribute_img": None,
                            "is_selected": False,
                            "is_custom": False
                        }
                    ]
                }
            ],
            "promotion_from_date": self.sendo_promotion_from_date,
            "promotion_to_date": self.sendo_promotion_to_date,
            "is_promotion": self.sendo_is_promotion or True,
            "extended_shipping_package": {
                "is_using_instant": False,
                "is_using_in_day": False,
                "is_self_shipping": False,
                "is_using_standard": True,
                "is_using_eco": True
            },
            "variants": [
                {
                    "variant_attributes": [
                        {
                            "attribute_id": 0,
                            "attribute_code": None,
                            "option_id": 0
                        }
                    ],
                    "variant_sku": None,
                    "variant_price": 0,
                    "variant_promotion_start_date": None,
                    "variant_promotion_end_date": None,
                    "variant_special_price": 0,
                    "variant_quantity": 0
                }
            ],
            "is_config_variant": False,
            "special_price": self.sendo_special_price,
            "voucher": {
                "product_type": 1,
                "start_date": None,
                "end_date": None,
                "is_check_date": None
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + current_seller.token_connection
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.json()["success"]:
            pass
        else:
            raise ValidationError(_('Create or Update Product Fail in Sync with Sendo.'))
