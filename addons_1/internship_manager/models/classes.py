from odoo import api, fields, models


class classes(models.Model):
    _name = 'classes'
    _description = 'class list'
    _rec_name = 'class_name'

    class_name = fields.Char(string='Class name', required=True)
    orientation_class = fields.Char(string='Orientation class')
    course_id = fields.Many2one(comodel_name='courses', string='Course name', domain="[('active_course','!=','finished')]")

    _sql_constraints = [
        ('class_name', 'UNIQUE (class_name)', 'class all already exists')]