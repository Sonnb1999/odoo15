from email.policy import default
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from . import students
import datetime


class instructors(models.Model):
    _name = 'instructors'
    _description = 'instructors list'
    _rec_name = 'student_id'

    # def _set_domain(self):
    #     ids = self.env['instructors']
    #     return {
    #         'domain': {'student_id': [('id', '=', ids.student_id)] }
    #     }

    student_count = fields.Char(
        string='number of student', compute='compute_count_student', store=False)
    student_id = fields.Many2one(
        comodel_name='students', string='student name', required=True, domain="[('instructor_id','=',student_id)]")

    student_image = fields.Binary(related='student_id.student_image')

    student_code = fields.Char(
        related='student_id.student_code', string='student code', store=True, default="0")

    birthday = fields.Date(related='student_id.birthday', string='birthday')

    activ_i = fields.Boolean(string='activ_i')

    class_id = fields.Many2one(
        related='student_id.class_id', string='class name', store=True)

    course_id = fields.Many2one(
        related='class_id.course_id', string='course name', store=True)

    teacher_id = fields.Many2one(
        comodel_name='teachers', string='teacher name')

    plan_id = fields.One2many(related='course_id.plan_id', string="plans")

    email = fields.Char(related='teacher_id.email', string='email')
    phone_number = fields.Char(
        related='teacher_id.phone_number', string='phone number')
    plan_time = fields.Boolean(string="time True")

    user_id = fields.Many2one(related='teacher_id.user_id', string="user_id")

    _sql_constraints = [
        ('student_id', 'UNIQUE (student_id)', 'student already exists')]

    @api.constrains('student_id')
    def studentValidate(self):
        for record in self:
            # record.student_id.id same ['student_id','id']
            student_id = record.search_count(
                [('student_id', '=', record.student_id.id)])
            print(student_id)
            if student_id > 1:
                raise ValidationError(_("Student already exists"))

    @api.constrains('teacher_id')
    def count_student(self):
        if self.teacher_id:
            for record in self:
                student_count_def = record.search_count(
                    [('teacher_id', '=', record.teacher_id.id)])
                if student_count_def > 3:
                    raise ValidationError(_("Teachers have enough students"))

    @api.onchange('teacher_id')
    def compute_count_student(self):
        if self.student_count:
            for record in self:
                student_count_def = record.search_count(
                    [('teacher_id', '=', record.teacher_id.id)])
                if student_count_def >= 3:
                    self.student_count = 'Teachers have enough students'
                else:
                    self.student_count = str(student_count_def)
        else:
            self.student_count = str(0)
