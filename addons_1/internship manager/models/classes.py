from odoo import api,fields,models

class classes(models.Model):
    _name = 'classes'
    _description = 'class list'
    _rec_name = 'class_name'

    class_name = fields.Char(string='class name')
    orientation_class = fields.Char(string='orientation_class')
    course_id = fields.Many2one(comodel_name='courses',string='course name')

    _sql_constraints = [('class_name','UNIQUE (class_name)','class all already exists')]