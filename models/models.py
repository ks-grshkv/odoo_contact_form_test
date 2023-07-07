# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class /../../../../mnt/extra-addons/contact_form_module(models.Model):
#     _name = '/../../../../mnt/extraons/contact_form_module'
#     _description = '/../../../../mnt/extrntact_form_module'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    # _name = 'contact_form_module'

    experience = fields.Float()
    department = fields.Char()
    origin_country = fields.Selection(
        [('uk', 'United Kingdom'), ('usa', 'United States')],
        tracking=True,
        string='Origin Country')
    # first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    has_first_name = fields.Boolean(
        compute='_compute_has_firstname',
        string="has first name", default=False)
    # name = fields.Char(
    #     compute='_compute_name', recursive=True, store=True, index=True)

    channel_ids = fields.Many2many(
        relation='mail_channel_library_book_partner')
    meeting_ids = fields.Many2many(relation='mmetings_partner')

    @api.onchange("experience")
    def _onchange_experience(self):
        if self.experience < 0:
            self.experience = 0

    def _compute_has_firstname(self):
        if self.name:
            print('AAAAAAA', self.name)
            self.has_first_name = True
        else:
            print('NNNNNA')
            self.has_first_name = False
    
    def _compute_name(self):
        self.name = str(str(self.first_name) + ' ' + str(self.last_name))

    @api.constrains("department")
    def _check_department(self):
        if not self.department.isalpha():
            raise ValidationError("The department field can accept only alphabetic characters")

    @api.constrains("company_name")
    def _check_company_name(self):
        if self.company_name:
            if not str(self.company_name).isalnum():
                raise ValidationError("nnanana2")


class ResCompany(models.Model):
    _inherit = 'res.company'
    # _name = 'contact_form_module'

    @api.constrains("name")
    # не работает
    def _check_name(self):
        if self.name and not self.name.isalnum():
            print('AAAASDADSDSADAD', self.name)
            raise ValidationError("The company name field can accept only alphanumeric characters")
