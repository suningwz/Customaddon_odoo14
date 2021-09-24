# -*- coding: utf-8 -*-
# from odoo import http


# class ShopiftOdoo(http.Controller):
#     @http.route('/shopift_odoo/shopift_odoo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/shopift_odoo/shopift_odoo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('shopift_odoo.listing', {
#             'root': '/shopift_odoo/shopift_odoo',
#             'objects': http.request.env['shopift_odoo.shopift_odoo'].search([]),
#         })

#     @http.route('/shopift_odoo/shopift_odoo/objects/<model("shopift_odoo.shopift_odoo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('shopift_odoo.object', {
#             'object': obj
#         })
