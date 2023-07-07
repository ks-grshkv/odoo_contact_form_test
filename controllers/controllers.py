# -*- coding: utf-8 -*-
# from odoo import http


# class /../../../../mnt/extra-addons/contactFormModule(http.Controller):
#     @http.route('//../../../../mnt/extra-addons/contact_form_module//../../../../mnt/extra-addons/contact_form_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//../../../../mnt/extra-addons/contact_form_module//../../../../mnt/extra-addons/contact_form_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('/../../../../mnt/extra-addons/contact_form_module.listing', {
#             'root': '//../../../../mnt/extra-addons/contact_form_module//../../../../mnt/extra-addons/contact_form_module',
#             'objects': http.request.env['/../../../../mnt/extra-addons/contact_form_module./../../../../mnt/extra-addons/contact_form_module'].search([]),
#         })

#     @http.route('//../../../../mnt/extra-addons/contact_form_module//../../../../mnt/extra-addons/contact_form_module/objects/<model("/../../../../mnt/extra-addons/contact_form_module./../../../../mnt/extra-addons/contact_form_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/../../../../mnt/extra-addons/contact_form_module.object', {
#             'object': obj
#         })
