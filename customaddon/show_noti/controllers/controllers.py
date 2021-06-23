# -*- coding: utf-8 -*-
# from odoo import http


# class ShowNoti(http.Controller):
#     @http.route('/show_noti/show_noti/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/show_noti/show_noti/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('show_noti.listing', {
#             'root': '/show_noti/show_noti',
#             'objects': http.request.env['show_noti.show_noti'].search([]),
#         })

#     @http.route('/show_noti/show_noti/objects/<model("show_noti.show_noti"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('show_noti.object', {
#             'object': obj
#         })
