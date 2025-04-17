# -*- coding: utf-8 -*-
# from odoo import http


# class /home/cristian/work18/library/libraryPortal/(http.Controller):
#     @http.route('//home/cristian/work18/library/library_portal///home/cristian/work18/library/library_portal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//home/cristian/work18/library/library_portal///home/cristian/work18/library/library_portal//objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('/home/cristian/work18/library/library_portal/.listing', {
#             'root': '//home/cristian/work18/library/library_portal///home/cristian/work18/library/library_portal/',
#             'objects': http.request.env['/home/cristian/work18/library/library_portal/./home/cristian/work18/library/library_portal/'].search([]),
#         })

#     @http.route('//home/cristian/work18/library/library_portal///home/cristian/work18/library/library_portal//objects/<model("/home/cristian/work18/library/library_portal/./home/cristian/work18/library/library_portal/"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/home/cristian/work18/library/library_portal/.object', {
#             'object': obj
#         })

