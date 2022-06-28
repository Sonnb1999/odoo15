from email.policy import default
from odoo import fields, api, models
import datetime

from datetime import timedelta


class estate_property(models.Model):
    _name = 'estate.property'
    _description = "odoo exercise"
    _rec_name = "name"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Availability form", copy=True, default=datetime.datetime.today() + timedelta(100))
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True)
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
        [('new', 'New'), ('old', 'Old')], string="Status")

    user_id = fields.Many2one(comodel_name='res.users', string='Buyer')
    partner_id = fields.Many2one("res.partner", string="Partner", copy=False)

    estate_type = fields.Many2one(
        "estate.property.type", string="Property type")
    estate_tag = fields.Many2many("estate.property.tag", string="Property tag")

    estate_offer = fields.One2many(
        "estate.property.offer", inverse_name="property_id", string="Property offer")

    partner_id = fields.Many2one("res.partner")

    total_area = fields.Float(compute="_compute_total",
                              string="Total Area (sqm)")
    bet_offer = fields.Float(compute="_compute_total_offer", string="Bet offer", default = 0)

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = float(record.living_area + record.garden_area)

    @api.depends("estate_offer.price")
    def _compute_total_offer(self):
        for record in self:
            if record.estate_offer:
                record.bet_offer = max(record.estate_offer.mapped('price'))
                

