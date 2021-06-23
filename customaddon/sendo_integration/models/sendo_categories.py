import requests
import json
from odoo import fields, models, api


class SendoCategories(models.Model):
    _name = "sendo.categories"
    _description = "Categories"

    category_id = fields.Char(string='Category ID')
    name = fields.Text(string='Name')
    level = fields.Integer(string='Primary')
    sendo_parent_id = fields.Char(string='Sendo Parent ID')
    parent_id = fields.Many2one(comodel_name='sendo.categories', string='Parent Category')

    product_get_token = fields.Many2many('sendo.connect.wizard')
    token_sendo = fields.Char(related='product_get_token.token_connection')

    def get_categories_sendo(self):
        for rec in self:
            url = "https://open.sendo.vn/api/partner/category/0"

            payload = {}
            headers = {
                'Authorization': 'Bearer ' + rec.token_sendo
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            categories = response.json()
            val = {}
            if categories:
                for cate in categories:
                    try:
                        if ('id' and 'name' and 'level') in cate:
                            val['category_id'] = cate['id']
                            val['name'] = cate['name']
                            val['level'] = cate['level']
                    except Exception as e:
                        print(e)
                    existed_category = self.env['sendo.categories'].search([('category_id', '=', cate['id'])], limit=1)
                    if len(existed_category) < 1:
                        self.create(val)
                    else:
                        existed_category.write(val)

    def get_child_categories_sendo(self):
        has_not_called_api = self.env['tiki.categories'].sudo().search([('level', '!=', 4)])
        for a in has_not_called_api:
            url = 'https://open.sendo.vn/api/partner/category/' + str(a['category_id'])

            payload = {}
            headers = {
                'Authorization': 'Bearer ' + self.token_sendo
            }

            response_raw = requests.request("GET", url, headers=headers, data=payload)
            response = response_raw.json()
            val = {}
            if response:
                for res in response:
                    try:
                        if ('id' and 'name' and 'level') in res:
                            val['category_id'] = res['id']
                            val['name'] = a.name + ' / ' + res['name']
                            val['level'] = res['level']
                            val['sendo_parent_id'] = a.category_id
                            val['parent_id'] = a.id
                            self.create(val)
                    except Exception as e:
                        print(e)
