from email.policy import default
from datetime import timedelta
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
    school_year = fields.Char(string='school_year', tracking=True)
    educational_system = fields.Selection(Type_of_education, tracking=True)
    type_of_internship = fields.Selection(Type_of_internship, tracking=True)
    start_time = fields.Date(string='start_time', tracking=True)
    end_time = fields.Date(string='end_time', tracking=True)
    student_ids = fields.One2many(
        'students', 'course_id', string='students', tracking=True)
    instructor_ids = fields.One2many(
        'instructors', 'course_id', string='instructors', tracking=True)

    active_course = fields.Selection([
        ('not_started_yet', 'not started yet'),
        ('started', 'started'),
        ('finished', 'finished'),
    ], string="active course", default='not_started_yet', tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string="status", default="draft", required=True)

    tag_partners = fields.Many2many('partners', string="Tags", tracking=True)

    _sql_constraints = [
        ('course_name', 'UNIQUE (course_name)', 'Course all already exists')]

    @api.constrains('start_time', 'end_time')
    def time(self):
        for record in self:
            if record.start_time > record.end_time:
                raise ValidationError('start time < end time')

    def action_test(self):
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'ok',
                'type': 'rainbow_man'
            }
        }

    def action_draft(self):
        for record in self:
            record.state = "draft"

    def action_in_consultation(self):
        for record in self:
            record.state = "in_consultation"

    def action_done(self):
        for record in self:
            record.state = "done"
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'ok',
                    'type': 'rainbow_man'
                }
            }

    def action_cancel(self):
        for record in self:
            record.state = "cancel"

    @api.model
    def create(self, vals):
        print('odoo create course >>>>>', vals)
        # vals['type_of_internship'] = ''
        return super(courses, self).create(vals)

    def write(self, vals):
        return super().write(vals)

    @api.onchange('start_time', 'type_of_internship')
    def change_time(self):
        if self.start_time:
            for record in self:
                _start = record.start_time
                # _end = record.end_time
                if record.type_of_internship == "internship":
                    record.end_time = _start + timedelta(days=60)
                elif record.type_of_internship == "professional_practice":
                    record.end_time = _start + timedelta(days=30)
                elif record.type_of_internship == "graduation_thesis":
                    record.end_time = _start + timedelta(days=100)
