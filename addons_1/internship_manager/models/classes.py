from odoo import api, fields, models


class classes(models.Model):
    _name = 'classes'
    _description = 'class list'
    _rec_name = 'class_name'

    class_name = fields.Char(string='Class name', required=True)
    course_id = fields.Many2one(comodel_name='courses', string='Course name',
                                domain="[('active_course','!=','finished')]", ondelete="cascade")
    
    orientation_class_ids = fields.One2many(
        'orentation.class','class_id', tracking=True)
        
    _sql_constraints = [
        ('class_name', 'UNIQUE (class_name)', 'class all already exists')]

    
