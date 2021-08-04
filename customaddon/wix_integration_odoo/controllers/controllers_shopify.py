import string

from odoo import http
from odoo.http import request, Response
import shopify
import binascii
import os
import werkzeug
from werkzeug.utils import redirect
from werkzeug.http import dump_cookie
import random
import string

base_url = "https://odoo.website"


class ShopifyApp(http.Controller):
    @http.route('/shopify/auth/<string:name>', auth='public', website=False)
    def shopify_auth(self, name, **kw):

        is_app = http.request.env['shopify.app'].sudo().search([('app_name', '=', name)])

        shopify.Session.setup(api_key=is_app.api_key, secret=is_app.secret_key)
        shop_url = request.params['shop']
        callback_url = base_url + "/shopify/finalize/" + name
        scopes = ['read_products', 'read_orders']
        new_session = shopify.Session(shop_url, is_app.api_version)
        auth_url = new_session.create_permission_url(scopes, callback_url)
        print(auth_url)
        return werkzeug.utils.redirect(auth_url)

    @http.route('/shopify/finalize/<string:name>', auth='public', website=True)
    def shopify_finalize(self, name, **kwargs):
        request_params = request.params
        shop_url = request_params['shop']
        x = shop_url.split('.')
        shop_name = x[1]
        result_str = ''.join(random.choice(string.digits) for i in range(10))
        is_shop = http.request.env['shopify.shop'].sudo().search([('shop_owner', '=', shop_name)])
        is_app = http.request.env['shopify.app'].sudo().search([('app_name', '=', name)])
        if is_shop.shop_owner != shop_name:
            request.env['shopify.shop'].sudo().create({
                'shop_base_url': shop_url,
                'shop_owner': shop_name,
                'shop_user': shop_url,
                'shop_password': result_str
            })
        is_user = request.env['res.users'].sudo().search([('login', '=', shop_url)])
        if is_user.login != shop_url:
            request.env['res.users'].sudo().create({
                'name': shop_name,
                'login': shop_url,
                'password': str(result_str)
            })
        db = http.request.env.cr.dbname
        request.env.cr.commit()
        uid = request.session.authenticate(db, is_user.login, is_shop.shop_password)
        print(uid)
        session = shopify.Session(shop_url, is_app.api_version)
        access_token = session.request_token(request_params)
        is_shop_app = request.env['shopify.shop.app'].sudo().search([('token_shop_app', '=', access_token)])
        if is_shop_app.token_shop_app != access_token:
            request.env['shopify.shop.app'].sudo().create({
                'token_shop_app': access_token,
                'web_user': shop_url,
                'password_user': '1'
            })
        session = shopify.Session(shop_url, is_app.api_version, access_token)
        shopify.ShopifyResource.activate_session(session)
        return werkzeug.utils.redirect(
            'https://odoo.website/web#action=458&model=shopify.shop&view_type=kanban&cids=1&menu_id=329')
