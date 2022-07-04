from odoo import fields, api, models
import datetime

from odoo.exceptions import ValidationError

from datetime import timedelta


class estate_property(models.Model):
    _name = 'estate.property'
    _description = "odoo exercise"
    _rec_name = "name"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Availability form", copy=True, default=datetime.datetime.today() + timedelta(100))
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(
        string="Selling price", readonly=True,)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden area")
    garden_orientation = fields.Selection([("north", "North"), ("south", "South"), (
        "east", "East"), ("west", "West")], string="garden_orientation")

    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        [('new', 'new'), ('old', 'Offer Received'),('offer_accepted','Offer Accepted'),('sold', 'Sold'), ('cancel', 'Cancel')], string="Status", default="new")

    user_id = fields.Many2one(comodel_name='res.users', string='user')
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    # group_expand='_expand_status'
    estate_type = fields.Many2one(
        "estate.property.type", string="Property type",)
    estate_tag = fields.Many2many("estate.property.tag", string="Property tag")

    estate_offer = fields.One2many(
        "estate.property.offer", inverse_name="property_id", string="Property offer", default=0, ondelete='cascade',)

    total_area = fields.Float(compute="_compute_total",
                              string="Total Area (sqm)")
    bet_offer = fields.Float(
        compute="_compute_total_offer", string="Bet offer", default=0)


    # def _expand_status(self, states, domain, order):
    #     return [key for key, val in type(self).state.selection]

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = float(record.living_area + record.garden_area)

    @api.depends("estate_offer.price")
    def _compute_total_offer(self):
        for record in self:
            if record.estate_offer:
                record.bet_offer = max(record.estate_offer.mapped('price'))
            else:
                record.bet_offer = 0

    def action_selling(self):
        for record in self:
            if record.estate_offer:
                offer_filter = record.estate_offer.filtered(lambda a: a.state == "accepted")
                record.selling_price = offer_filter.price

                # print("test......:",a.price)
            else:
                record.selling_price = 0

    @api.constrains("expected_price")
    def check_expected_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError(
                    "A property expected price must be strictly positive")

    @api.onchange('garden')
    def change_garden(self):
        for record in self:
            if record.garden == False:
                record.garden_area = 0
                record.garden_orientation = None
            else:
                record.garden_area = 10
                record.garden_orientation = "north"

    def action_sold(self):
        for record in self:
            if record.state:
                if record.state == "cancel":
                    raise ValidationError(
                        "can not change status when status is cancel")
                else:
                    record.state = "sold"

    def action_cancel(self):
        for record in self:
            record.state = "cancel"

    # @api.depends("estate_offer.state")
    # def change_form(self):
    #     for record in self:
    #         if record.estate_offer.state:
    #             if record.estate_offer.state == "accepted":
    #                 record.partner_id = record.estate_offer.partner_id
    #                 record.selling_price = record.estate_offer.price
