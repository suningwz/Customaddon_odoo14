import requests
from odoo import fields, models, api


class SendoCategories(models.Model):
    _name = "sendo.categories"
    _description = "Categories"

    category_id = fields.Char(string='Category ID')
    name = fields.Text(string='Name')
    status = fields.Char(string='Status')
    is_primary = fields.Boolean(string='Primary')
    has_called = fields.Boolean(string='Call from Sendo', default=False)
    sendo_parent_id = fields.Char(string='Sendo Parent ID')
    parent_id = fields.Many2one(comodel_name='sendo.categories', string='Parent Category')

    def get_categories_sendo(self):
        current_seller = self.env['sendo.seller'].sudo().search([])[0]
        url = "https://api-sellercenter.sendo.vn/integration/categories"
        payload = {
        }
        headers = {
            'sendo-api': current_seller.secret,
            'User-Agent': current_seller.user_agent,
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        categories = response.json()
        val = {}
        if categories:
            for cate in categories:
                try:
                    if ('id' and 'name' and 'status' and 'is_primary') in cate:
                        val['category_id'] = cate['id']
                        val['name'] = cate['name']
                        val['status'] = cate['status']
                        val['is_primary'] = cate['is_primary']
                        val['has_called'] = False
                        val['sendo_parent_id'] = 2
                except Exception as e:
                    print(e)
                existed_category = self.env['sendo.categories'].search([('category_id', '=', cate['id'])], limit=1)
                if len(existed_category) < 1:
                    self.create(val)
                else:
                    existed_category.write(val)

    def get_child_categories_sendo(self):
        current_seller = self.env['sendo.seller'].sudo().search([])[0]
        has_not_called_api = self.env['sendo.categories'].sudo().search(
            [('has_called', '=', False), ('is_primary', '=', False)])
        for a in has_not_called_api:
            url = 'https://api-sellercenter.sendo.vn/integration/categories' + '?parent_id=' + str(a['category_id'])
            payload = {
            }
            headers = {
                'sendo-api': current_seller.secret,
                'User-Agent': current_seller.user_agent,
            }
            response_raw = requests.request("GET", url, headers=headers, data=payload)
            response = response_raw.json()
            val = {}
            if response:
                for res in response:
                    try:
                        if ('id' and 'name' and 'status' and 'is_primary') in res:
                            val['category_id'] = res['id']
                            val['name'] = a.name + ' / ' + res['name']
                            val['status'] = res['status']
                            val['is_primary'] = res['is_primary']
                            val['has_called'] = False
                            val['sendo_parent_id'] = a.category_id
                            val['parent_id'] = a.id
                            self.create(val)
                    except Exception as e:
                        print(e)
            a.has_called = True

# # Dungnh #####################################
#     def request_get(self, parent_id):
#         current_seller = self.env['sendo.seller'].sudo().search([])[0]
#         url = 'https://api-sellercenter.sendo.vn/integration/categories' + '?parent_id=' + str(parent_id)
#         payload = {
#         }
#         headers = {
#             'sendo-api': current_seller.secret,
#             'User-Agent': current_seller.user_agent,
#         }
#         data_raw = requests.request("GET", url, headers=headers, data=payload)
#         data = data_raw.json()
#         if len(data) > 1:
#             for x in data:
#                 # create vao odoo
#                 self.env['sendo.categories'].sudo().create({
#                     'category_id': x['id']
#                 })
#                 self.request_get(x['id'])
#         else:
#             if data[0]['status_code'] == 404:
#                 pass
#
#     def get_categories_sendo(self):
#         current_seller = self.env['sendo.seller'].sudo().search([])[0]
#         url = 'https://api-sellercenter.sendo.vn/integration/categories'
#         payload = {
#         }
#         headers = {
#             'sendo-api': current_seller.secret,
#             'User-Agent': current_seller.user_agent,
#         }
#         response_raw = requests.request("GET", url, headers=headers, data=payload)
#         response = response_raw.json()
#         if response:
#             for rec in response:
#                 self.request_get(rec['id'])
#                 print(self.request_get(rec['id']))
