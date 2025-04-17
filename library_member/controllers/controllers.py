# -*- coding: utf-8 -*-
# from odoo import http


# class /home/cristian/work18/library/libraryApp/libraryMember/(http.Controller):
#     @http.route('//home/cristian/work18/library/library_app/library_member///home/cristian/work18/library/library_app/library_member/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//home/cristian/work18/library/library_app/library_member///home/cristian/work18/library/library_app/library_member//objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('/home/cristian/work18/library/library_app/library_member/.listing', {
#             'root': '//home/cristian/work18/library/library_app/library_member///home/cristian/work18/library/library_app/library_member/',
#             'objects': http.request.env['/home/cristian/work18/library/library_app/library_member/./home/cristian/work18/library/library_app/library_member/'].search([]),
#         })

#     @http.route('//home/cristian/work18/library/library_app/library_member///home/cristian/work18/library/library_app/library_member//objects/<model("/home/cristian/work18/library/library_app/library_member/./home/cristian/work18/library/library_app/library_member/"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/home/cristian/work18/library/library_app/library_member/.object', {
#             'object': obj
#         })

