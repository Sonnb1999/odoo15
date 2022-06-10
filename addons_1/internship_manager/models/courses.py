from email.policy import default

from pkg_resources import require
from odoo import api, fields, models
from odoo.exceptions import ValidationError
Type_of_education = [('formal_university', 'Formal university'),
                     ('affiliated_university', 'Affiliated university')]

Type_of_internship = [('internship', 'Internship'), (
    'professional_practice', 'Professional practice'), ('graduation_thesis', 'Graduation thesis')]


class courses(models.Model):
    _name = 'courses'
    _description = 'course list'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'course_name'

    course_name = fields.Char(string='course name',
                              required=True, tracking=True, help="the name of the course")
    school_year = fields.Char(string='school_year')
    educational_system = fields.Selection(Type_of_education)
    type_of_internship = fields.Selection(Type_of_internship)
    start_time = fields.Date(string='start_time', tracking=True)
    end_time = fields.Date(string='end_time', tracking=True)
    student_ids = fields.One2many(
        'students', 'course_id', string='students')
    instructor_ids = fields.One2many(
        'instructors', 'course_id', string='instructors')

    active_course = fields.Selection([
        ('not_started_yet', 'not started yet'),
        ('started', 'started'),
        ('finished', 'finished'),
    ], string="active course", default='not_started_yet')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string="status", default="draft", required=True)

    _sql_constraints = [
        ('course_name', 'UNIQUE (course_name)', 'Course all already exists')]

    @api.constrains('start_time', 'end_time')
    def time(self):
        for record in self:
            if record.start_time > record.end_time:
                raise ValidationError('start time < end time')
    
    def action_test(self):
        return {
            'effect':{
                'fadeout':'slow',
                'message':'ok',
                'type':'rainbow_man'
            }
        }
