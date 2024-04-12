# -*- coding: utf-8 -*-
# from odoo import http


# class TscSeniatDispatchNote(http.Controller):
#     @http.route('/tsc__seniat_dispatch_note/tsc__seniat_dispatch_note', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tsc__seniat_dispatch_note/tsc__seniat_dispatch_note/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tsc__seniat_dispatch_note.listing', {
#             'root': '/tsc__seniat_dispatch_note/tsc__seniat_dispatch_note',
#             'objects': http.request.env['tsc__seniat_dispatch_note.tsc__seniat_dispatch_note'].search([]),
#         })

#     @http.route('/tsc__seniat_dispatch_note/tsc__seniat_dispatch_note/objects/<model("tsc__seniat_dispatch_note.tsc__seniat_dispatch_note"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tsc__seniat_dispatch_note.object', {
#             'object': obj
#         })
