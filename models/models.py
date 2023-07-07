from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo import _, exceptions


class EmptyNamesError(exceptions.ValidationError):
    def __init__(self, record, value=None):
        value = value or _("No name is set.")
        self.record = record
        self._value = value
        self._name = _("Error(s) with partner %d's name.") % record.id
        self.args = (self._name, value)


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
    has_first_name = fields.Boolean()
    name = fields.Char(
        compute='_compute_name', required=False,
        precompute=True,
        store=True,
        recursive=True, index=True)
    # display_name = fields.Char('_compute_name', required=False, precompute=True, recursive=True, index=True)

    channel_ids = fields.Many2many(
        relation='mail_channel_library_book_partner')
    meeting_ids = fields.Many2many(relation='mmetings_partner')


    @api.constrains("firstname", "lastname")
    def _check_name(self):
        """Ensure at least one name is set."""
        for record in self:
            if all(
                (
                    record.type == "contact" or record.is_company,
                    not (record.firstname or record.lastname),
                )
            ):
                raise EmptyNamesError(record)

    @api.onchange("experience")
    def _onchange_experience(self):
        if self.experience < 0:
            self.experience = 0

    @api.onchange("first_name")
    def _compute_has_firstname(self):
        if self.first_name:
            self.has_first_name = True
        else:
            self.has_first_name = False
    
    # @api.onchange("first_name", "last_name")
    # def _recompute_display_name(self):
    #     self.display_name = str(str(self.first_name) + ' ' + str(self.last_name))

    # def _compute_display_name(self):
    #     self.display_name = str(str(self.first_name) + ' ' + str(self.last_name))

    @api.onchange("first_name", "last_name")
    def _recompute_name(self):
        self.name = str(str(self.first_name) + ' ' + str(self.last_name))
        # self.display_name = self.name

    def _compute_name(self):
        self.name = str(str(self.first_name) + ' ' + str(self.last_name))
        # self.display_name = self.name

    @api.constrains("department")
    def _check_department(self):
        if self.department:
            if not self.department.isalpha():
                raise ValidationError(
                    "The department field can accept only alphabetic characters")

    @api.constrains("company_name")
    def _check_company_name(self):
        if self.company_name:
            if not str(self.company_name).isalnum():
                raise ValidationError("The company name field can accept only alphanumeric characters")
