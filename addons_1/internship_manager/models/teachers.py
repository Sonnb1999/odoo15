import re
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class teachers(models.Model):
    _name = 'teachers'
    _description = 'teacher list'
    _rec_name = 'teacher_name'

    teacher_name = fields.Char(string='teacher name', required=True)
    teacher_image = fields.Binary(string='teacher image')
    email = fields.Char(string='email', required=True)
    password = fields.Char(string='Password')
    birthday = fields.Date(string='birthday')
    phone_number = fields.Char(string='phone number')
    address = fields.Char(string='address')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', default='male')

    teacher_country = fields.Many2one(
        comodel_name='res.country', string='country', store=True,default= 241)
    teacher_state = fields.Many2one(
        'res.country.state', string="State", store=True)

    class_id = fields.Many2one(comodel_name='classes', string='class name')

    @api.onchange('teacher_country')
    def set_values_to(self):
        if self.teacher_country:
            ids = self.env['res.country.state'].search(
                [('country_id', '=', self.teacher_country.id)])
            return {
                'domain': {'teacher_state': [('id', 'in', ids.ids)], }
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

    @api.model
    def create(self, vals):
        if vals.get('user_id', False):
            user_id = self.env['res.users'].browse(vals.get('user_id', False))
            # vals.update(
            #     {'teacher_id': user_id.teacher_id and user_id.teacher_id.id or False})
        return super(teachers, self).create(vals)

    # @api.constrains('student_name')
    # def cout_student(self):
    #     for record in self:
    #         pass
