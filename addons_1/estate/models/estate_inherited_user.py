from odoo import models,fields,api


class inherited_user(models.Model):
    _inherit = "res.users"
    property_ids = fields.One2many("estate.property","user_id")