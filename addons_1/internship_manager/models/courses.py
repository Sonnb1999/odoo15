from odoo import api, fields, models
type_of_education = [('formal university', 'formal university'),
                     ('affiliated university', 'affiliated university')]

Type_of_internship = [('internship', 'internship'), (
    'professional practice', 'professional practice'), ('graduation thesis', 'graduation thesis')]


class courses(models.Model):
    _name = 'courses'
    _description = 'course list'
    _rec_name = 'course_name'

    course_name = fields.Char(string='course name', required=True)
    school_year = fields.Char(string='school_year')
    educational_system = fields.Selection(type_of_education)
    type_of_internship = fields.Selection(Type_of_internship)
    start_time = fields.Date(string='start_time')
    end_time = fields.Date(string='end_time')

    _sql_constraints = [
        ('course_name', 'UNIQUE (course_name)', 'Course all already exists')]
