from odoo import fields, api, models
import datetime


class estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "estate type"
    _rec_name = "name"
    name = fields.Char("Title")


class estate_tag(models.Model):
    _name = "estate.property.tag"
    _description = "estate tag"
    _rec_name = "name"

    name = fields.Char("Title")


class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "estate offer"
    _rec_name = "partner_id"

    price = fields.Integer("price")
    state = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False)

    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    property_id = fields.Many2one(
        "estate.property", "Property", required=True)

    validity = fields.Integer("validity(days)", default=7)
    date_deadline = fields.Date("date_deadline", compute = "compute_date")

    @api.depends("validity")
    def compute_date(self):
        for record in self:
            if record.validity:
                record.date_deadline = datetime.date.today() + datetime.timedelta(record.validity)

    # @api.depends("validity")
    # def compute_date(self):
    #     for record in self:
    #         if record.validity:
    #             record.date_deadline = datetime.date.today() + datetime.timedelta(record.validity)

