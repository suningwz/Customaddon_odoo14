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


class WixApp(http.Controller):
    @http.route('/signup?token=<string:name>', auth='public', website=False)
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


