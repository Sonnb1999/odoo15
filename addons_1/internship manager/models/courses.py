from odoo import api,fields,models

class courses(models.Model):
    _name = 'courses'
    _description = 'course list'
    _rec_name = 'course_name'

    course_name = fields.Char(string='course name')
    school_year = fields.Char(string='school_year')
    educational_system = fields.Char(string='educational_system')
    type_of_internship = fields.Char(string='type_of_internship')
    start_time = fields.Date(string='start_time')
    end_time = fields.Date(string='end_time')

    _sql_constraints = [('course_name','UNIQUE (course_name)','Course all already exists')]