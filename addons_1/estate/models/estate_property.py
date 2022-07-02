from email.policy import default
from re import A
from signal import raise_signal
from odoo import fields, api, models
import datetime

from odoo.exceptions import ValidationError


class estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "estate type"
    _rec_name = "name"
    _order = "name"

    name = fields.Char("Title")
    sequence = fields.Integer("Sequence", default=0)
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", "offer id")
    offer_count = fields.Integer("offer_count", compute="_compute_offer_count")
    property_id = fields.One2many("estate.property", "estate_type")
    _sql_constraints = [('uniq_name', 'unique(name)',
                         "The name of this POS Session must be unique !")]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        if self.offer_ids:
            for record in self:
                record.offer_count = len(record.offer_ids)
        else:
            self.offer_count = 0

    def action_count(self):
        return {
            'name': ('offer'),
            'res_model': 'estate.property.offer',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'view_type': 'list,form',
            'target': 'current',
            'domain': [('property_type_id', '=', self.id)],
        }


class estate_property_tag(models.Model):
    _name = "estate.property.tag"
    _description = "estate tag"
    _rec_name = "name"
    _order = "name"

    name = fields.Char("Title")
    color = fields.Integer("Color")
    _sql_constraints = [('uniq_name', 'unique(name)',
                         "The name of this POS Session must be unique !")]


class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "estate offer"
    _rec_name = "partner_id"
    _order = "price desc"

    price = fields.Integer("price")
    state = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False)
    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    property_id = fields.Many2one(
        "estate.property", "Property", required=True, ondelete='cascade', store=True)

    property_type_id = fields.Many2one(
        related='property_id.estate_type', string="type")
    validity = fields.Integer("validity(days)", default=7)
    date_deadline = fields.Date(
        "date_deadline", compute="compute_date", readonly=False)

    @api.depends("validity")
    def compute_date(self):
        for record in self:
            if record.validity:
                record.date_deadline = datetime.date.today() + datetime.timedelta(record.validity)

    @api.onchange("price")
    def change_price(self):
        for record in self:
            record.state = None

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

                # print('test', 100 - record.price / ex)
                # print('test1', 100 - record.price / ex)
                if len(offer_id) > 1:
                    raise ValidationError("only accepted")
                else:
                    if 100 - record.price / ex <= 10 or 100 - record.price / ex <= 0:
                        record.state = "accepted"
                        record.property_id.selling_price = record.price
                        record.property_id.partner_id = record.partner_id
                        record.property_id.state = "offer_accepted"

                    else:
                        raise ValidationError(
                            "that the selling price cannot be lower than 90% of the expected price")

    def action_refused(self):
        for record in self:
            record.state = "refused"
            record.property_id.selling_price = 0
            record.property_id.partner_id = None
            record.property_id.state = "old"


    # @api.onchange("state")
    # def change_state(self):
    #     for record in self:
    #         if record.state == "accepted":
    #             record.property_id.selling_price = record.price
    #             record.property_id.partner_id = record.partner_id
    #             record.property_id.state = "offer_accepted"

    #         else:
    #             record.property_id.selling_price = 0
    #             record.property_id.partner_id = None
