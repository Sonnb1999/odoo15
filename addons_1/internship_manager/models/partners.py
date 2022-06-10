from odoo import api,fields,models

class partners(models.Model):
    _name = 'partners'
    _description = 'partner list'
    _rec_name = 'partner_name'

    partner_name = fields.Char(string='Name')
    partner_active  = fields.Boolean(string='Active')
    color  = fields.Integer(string='Color')
    color2 = fields.Char(string='Color2')
    