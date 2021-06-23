import requests
from odoo.exceptions import UserError, ValidationError
from odoo import fields, models, api, _


class SendoSeller(models.Model):
    _name = "sendo.seller"
    _description = "Seller"

    seller_id = fields.Char(string='Seller ID')
    code = fields.Char(string='Code')
    contract_code = fields.Char(string='Contact Code')
    name = fields.Char(string='Name')
    logo = fields.Char(string='Logo')
    hotline = fields.Char(string='Hotline')
    email = fields.Char(string='Email')
    connect_to = fields.Char(string='Connect to')
    secret = fields.Char(string='Secret')
    user_agent = fields.Text(string='User Agent')

    def get_seller_sendo(self):
        exited_record = self.env['sendo.seller'].sudo().search([])[0]
        url = "https://api-sellercenter.sendo.vn/integration/sellers"
        payload = {}
        headers = {
            'sendo-api': exited_record.secret,
            'User-Agent': exited_record.user_agent,
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        seller = response.json()
        val = {}

        if (
                'id' and 'name' and 'code' and 'contract_code' and 'secret' and 'email' and 'connect_to' and 'logo') in seller:
            val['seller_id'] = seller['id']
            val['name'] = seller['name']
            val['code'] = seller['code']
            val['contract_code'] = seller['contract_code']
            val['secret'] = seller['secret']
            val['email'] = seller['email']
            val['connect_to'] = seller['connect_to']
            val['logo'] = seller['logo']
        existed_seller = self.env['sendo.seller'].search([('secret', '=', seller['secret'])], limit=1)
        if len(existed_seller) < 1:
            self.create(val)
        else:
            existed_seller.write(val)
