from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    experience = fields.Float()
    department = fields.Char()
    origin_country = fields.Selection(
        [('uk', 'United Kingdom'), ('usa', 'United States')],
        tracking=True,
        string='Origin Country')
    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    has_first_name = fields.Boolean(
        compute='_compute_has_firstname')
    name = fields.Char(
        compute='_compute_name', recursive=True, store=True, index=True)

    channel_ids = fields.Many2many(
        relation='mail_channel_library_book_partner')
    meeting_ids = fields.Many2many(relation='mmetings_partner')

    @api.onchange("experience")
    def _onchange_experience(self):
        if self.experience < 0:
            self.experience = 0

    def _compute_has_firstname(self):
        if self.name:
            self.has_first_name = True
        else:
            self.has_first_name = False

    def _compute_name(self):
        self.name = str(str(self.first_name) + ' ' + str(self.last_name))

    @api.constrains("department")
    def _check_department(self):
        if not self.department.isalpha():
            raise ValidationError(
                "The department field can accept only alphabetic characters")

    @api.constrains("company_name")
    def _check_company_name(self):
        if self.company_name:
            if not str(self.company_name).isalnum():
                raise ValidationError("The company name field can accept only alphanumeric characters")
