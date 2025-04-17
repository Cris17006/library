# -*- coding: utf-8 -*-
# from odoo import http


# class /home/cristian/work18/library/libraryApp/libraryMember/libraryCheckout/(http.Controller):
#     @http.route('//home/cristian/work18/library/library_app/library_member/library_checkout///home/cristian/work18/library/library_app/library_member/library_checkout/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//home/cristian/work18/library/library_app/library_member/library_checkout///home/cristian/work18/library/library_app/library_member/library_checkout//objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('/home/cristian/work18/library/library_app/library_member/library_checkout/.listing', {
#             'root': '//home/cristian/work18/library/library_app/library_member/library_checkout///home/cristian/work18/library/library_app/library_member/library_checkout/',
#             'objects': http.request.env['/home/cristian/work18/library/library_app/library_member/library_checkout/./home/cristian/work18/library/library_app/library_member/library_checkout/'].search([]),
#         })

#     @http.route('//home/cristian/work18/library/library_app/library_member/library_checkout///home/cristian/work18/library/library_app/library_member/library_checkout//objects/<model("/home/cristian/work18/library/library_app/library_member/library_checkout/./home/cristian/work18/library/library_app/library_member/library_checkout/"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/home/cristian/work18/library/library_app/library_member/library_checkout/.object', {
#             'object': obj
#         })

