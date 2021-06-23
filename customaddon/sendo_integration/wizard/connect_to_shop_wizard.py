import requests
import json
from odoo import fields, models, api
from odoo.http import request


class SellerConnectWizard(models.Model):
    _name = 'sendo.connect.wizard'
    _description = 'Connect to Sendo Integration'

    shop_key = fields.Char(string='My Shop key', stored=True, limited=1)
    secret_key = fields.Char(string='My Secret Key', stored=True, limited=1)
    token_connection = fields.Char()

    def get_token_sendo(self):
        for rec in self:
            url = "https://open.sendo.vn/login"
            payload = json.dumps({
                "shop_key": rec.shop_key,
                "secret_key": rec.secret_key
            })
            headers = {
                'Content-Type': 'application/json',
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            rec.token_connection = response.json()["result"]["token"]
            return rec.token_connection

    def update_token_sendo(self):
        self.token_connection = self.get_token_sendo()


