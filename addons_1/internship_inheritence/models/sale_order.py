from odoo import api, fields, models
from odoo.exceptions import ValidationError

class userTag(models.Model):
    _inherit = "sale.order"
    
    confirmed_user_id = fields.Many2one('res.users', string="confirmed user")
    
    def action_confirm(self):
        print('ok................')
        # super(userTag,self).action_confirm()
        # raise ValidationError('test from confirm')
