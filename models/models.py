from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    experience = fields.Float()
    department = fields.Char()
    phone = fields.Char(unaccent=False)
    email = fields.Char()
    origin_country = fields.Selection(
        [("uk", "United Kingdom"), ("usa", "United States")],
        tracking=True,
        string="Origin Country")
    first_name = fields.Char(string="First Name", default="")
    last_name = fields.Char(string="Last Name", default="")
    new_company_name = fields.Char(
            string="Company Name",
            default="",
            required=False
        )
    has_first_name = fields.Boolean(default=False)
    display_name = fields.Char(
            compute="_compute_display_name",
            recursive=True,
            store=True,
            index=True
        )

    name = fields.Char(
            compute="_recompute_name",
            required=False,
            precompute=True,
            readonly=False,
            store=True,
            recursive=True,
            index=True
        )

    channel_ids = fields.Many2many(
        relation="mail_channel_library_book_partner")
    meeting_ids = fields.Many2many(relation="meetings_partner")

    @api.constrains("first_name", "last_name", "new_company_name")
    def _check_name(self):
        for record in self:
            if record.type == "contact":
                if (
                    not record.is_company
                    and (not (record.first_name or record.last_name))
                ):
                    raise ValidationError(
                        "Please set at least one of the names")
            elif record.is_company and not record.new_company_name:
                raise ValidationError(
                        "Please set company name")

    @api.onchange("experience")
    def _onchange_experience(self):
        """
        Set experience to 0.00 if negative value is given.
        """
        if self.experience < 0:
            self.experience = 0

    @api.onchange("first_name")
    def _compute_has_firstname(self):
        if self.first_name:
            self.has_first_name = True
        else:
            self.has_first_name = False

    def concatenate_name(self, first_name, last_name, new_company_name):
        """
        Auxillary function.
        For indivifual partner: concatenates strings for first_name and last_name;
        For company partner: returns new_company_name.
        """
        if not first_name and not last_name:
            return new_company_name
        elif not first_name:
            return last_name
        elif not last_name:
            return first_name
        else:
            return first_name + " " + last_name

    @api.onchange("first_name", "last_name", "new_company_name")
    def _recompute_name(self):
        for record in self:
            record.name = self.concatenate_name(
                record.first_name,
                record.last_name,
                record.new_company_name
            )

    @api.constrains("department")
    def _check_department(self):
        if self.department:
            if not self.department.isalpha():
                raise ValidationError(
                    "The department field can accept "
                    + "only alphabetic characters"
                )

    @api.depends("first_name", "last_name", "new_company_name")
    def _compute_display_name(self):
        for record in self:
            record.display_name = self.concatenate_name(
                record.first_name,
                record.last_name,
                record.new_company_name
            )

    @api.constrains("new_company_name")
    def _check_company_name(self):
        if self.is_company:
            if self.new_company_name:
                if not str(self.new_company_name).isalnum():
                    raise ValidationError(
                        "The company name field can accept "
                        + "only alphanumeric characters"
                    )

    @api.constrains("phone", "email")
    def _not_empty_or_blank(self):
        if not self.phone or not self.email:
            raise ValidationError(
                "Please check that both email and phone fields are filled out"
            )
        phone = "".join(self.phone.split())
        email = "".join(self.email.split())
        if not phone or not email:
            raise ValidationError(
                "Please check that both email and phone fields are not blank"
            )
