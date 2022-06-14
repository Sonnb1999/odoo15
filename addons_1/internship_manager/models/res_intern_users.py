from odoo import fields, api, models
import re
from odoo.exceptions import ValidationError


class res_intern_users(models.Model):
    _name = "res.intern.users"
    _description = 'users intern'
    _rec_name = 'user_name'

    # information
    user_name = fields.Char(string='name', required=True)
    phone_number = fields.Char('Phone number')
    image = fields.Binary('Image')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', default='male')

    # address
    user_country = fields.Many2one(
        comodel_name='res.country', string='Country', store=True, default=241)
    user_state = fields.Many2one(
        'res.country.state', string="State", store=True)
    address = fields.Char(string='address')

    # email
    email = fields.Char(string='email', required=True)
    # relationship
    class_id = fields.Many2one(comodel_name='classes', string='class name')

    @api.onchange('user_country')
    def set_values_to(self):
        if self.user_country:
            ids = self.env['res.country.state'].search(
                [('country_id', '=', self.user_country.id)])
            return {
                'domain': {'user_state': [('id', 'in', ids.ids)], }
            }

    @api.constrains('phone_number')
    def validate_number(self):
        for record in self:
            if record.phone_number:
                if re.findall("[a-zA-Z]", record.phone_number):
                    raise ValidationError('the phone number is not true')
                elif len(record.phone_number) < 10 or len(record.phone_number) >= 11:
                    raise ValidationError('the phone number is wrong')
                else:
                    pass
