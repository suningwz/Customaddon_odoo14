from odoo import fields, models, api, _


class SendoSeller(models.Model):
    _name = "sendo.seller"
    _description = "Seller"

    shop_key = fields.Char(string='My Shop Key')
    secret_key = fields.Char(string='My Secret Key')
    token_connection = fields.Char(string='My Token')
    date_startup = fields.Date(string='Date Startup')
    sendo_order_date_from = fields.Date(string='Order Date From')
    sendo_order_date_to = fields.Date(string='Order Date To')
