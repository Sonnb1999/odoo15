from odoo import api,fields,models

class students(models.Model):
    _name = 'students'
    _description = 'student list'
    _rec_name = 'student_name'

    student_name = fields.Char(string='student name')
    student_image = fields.Binary(string='student image')
    student_code = fields.Char(string='student code')
    birthday = fields.Char(string='birthday')
    phone_number = fields.Char(string='phone number')
    address = fields.Char(string='address')
    class_id = fields.Many2one(comodel_name='classes', string='class name')
    course_id = fields.Many2one(related='class_id',string='course name',store=True)

    _sql_constraints = [('student_name','UNIQUE (student_name)','student all already exists')]