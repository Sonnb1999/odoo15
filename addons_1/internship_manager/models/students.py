from email.policy import default
from signal import raise_signal
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re


class students(models.Model):
    _name = 'students'
    _description = 'student list'
    _rec_name = 'student_name'

    student_name = fields.Char(string='student name', required=True)
    student_image = fields.Binary(string='student image')
    student_code = fields.Char(string='student code', required=True)
    birthday = fields.Date(string='birthday')
    phone_number = fields.Char(string='phone number')
    address = fields.Char(string='address')
    email = fields.Char(string='email', required=True)
    condition = fields.Selection(
        [('qualified', 'Qualified'), ('not_qualified_yet', 'Not qualified yet')], string='Condition', default='qualified')

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', default='male')
    instructor_id = fields.One2many(
        'instructors', 'student_id', 'instructor list')

    class_id = fields.Many2one(
        comodel_name='classes', string='class name', required=True)
    course_id = fields.Many2one(
        related='class_id.course_id', string='course name', store=True)

    _sql_constraints = [
        ('student_code', 'UNIQUE (student_code)', 'student already exists')]

    @api.onchange('user_id')
    def changeUser(self):
        for record in self:
            record.email = record.user_id.email

    @api.constrains('phone_number')
    def validate_number(self):
        for record in self:
            if record.phone_number:
                if re.findall("[a-zA-Z]", record.phone_number):
                    raise ValidationError('the phone number is not true')
                elif len(record.phone_number) < 10 or len(record.phone_number) > 11:
                    raise ValidationError('the phone number is wrong')
                else:
                    pass