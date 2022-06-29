from re import A
from signal import raise_signal
from odoo import fields, api, models
import datetime

from odoo.exceptions import ValidationError


class estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "estate type"
    _rec_name = "name"
    name = fields.Char("Title")

    _sql_constraints = [('uniq_name', 'unique(name)',
                         "The name of this POS Session must be unique !")]


class estate_tag(models.Model):
    _name = "estate.property.tag"
    _description = "estate tag"
    _rec_name = "name"

    name = fields.Char("Title")
    _sql_constraints = [('uniq_name', 'unique(name)',
                         "The name of this POS Session must be unique !")]


class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "estate offer"
    _rec_name = "partner_id"

    price = fields.Integer("price")
    state = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False)

    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    property_id = fields.Many2one(
        "estate.property", "Property", required=True, ondelete='cascade')

    validity = fields.Integer("validity(days)", default=7)
    date_deadline = fields.Date(
        "date_deadline", compute="compute_date", readonly=False)

    @api.depends("validity")
    def compute_date(self):
        for record in self:
            if record.validity:
                record.date_deadline = datetime.date.today() + datetime.timedelta(record.validity)

    @api.constrains("date_deadline")
    def change_date(self):
        for record in self:
            if record.date_deadline:
                # if record.date_deadline >= datetime.date.today():
                time_to_date = abs(record.date_deadline -
                                   datetime.date.today())
                record.validity = time_to_date.days

                # else:
                #     raise ValidationError("time is not true")

    def action_accepted(self):
        for record in self:
            record.state = "accepted"

            if record.property_id:
                offer_id = record.property_id.estate_offer.filtered(
                    lambda a: a.state == "accepted")
                    
                ex = record.property_id.expected_price / 100
                print('test',ex)
                if len(offer_id) > 1:
                    raise ValidationError("only accepted")
                else:
                    record.property_id.selling_price = record.price
                    record.property_id.partner_id = record.partner_id

    def action_refused(self):
        for record in self:
            record.state = "refused"
            record.property_id.selling_price = 0
            record.property_id.partner_id = None
