# -*- coding: utf-8 -*-
# from odoo import http


# class LibraryYubo(http.Controller):
#     @http.route('/library_yubo/library_yubo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/library_yubo/library_yubo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('library_yubo.listing', {
#             'root': '/library_yubo/library_yubo',
#             'objects': http.request.env['library_yubo.library_yubo'].search([]),
#         })

#     @http.route('/library_yubo/library_yubo/objects/<model("library_yubo.library_yubo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('library_yubo.object', {
#             'object': obj
#         })

