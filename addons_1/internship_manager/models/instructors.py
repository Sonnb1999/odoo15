from email.policy import default
from re import T

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import datetime

import mimetypes
from odoo.tools.mimetypes import guess_mimetype


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
        comodel_name='students', string='student name', required=True, domain="[('instructor_id','=',student_id)]", ondelete='cascade')

    student_image = fields.Binary(related='student_id.student_image')

    student_code = fields.Char(
        related='student_id.student_code', string='student code', store=True, default="0")

    birthday = fields.Date(related='student_id.birthday', string='birthday')

    active_i = fields.Boolean(string='active', default=True)

    class_id = fields.Many2one(
        related='student_id.class_id', string='class name', store=True)

    course_id = fields.Many2one(
        related='class_id.course_id', string='course name', store=True, group_expand='_read_group_stage_ids')

    teacher_id = fields.Many2one(
        comodel_name='teachers', string='teacher name')

    plan_id = fields.One2many(related='course_id.plan_id', string="plans")

    email = fields.Char(related='teacher_id.email', string='email')
    phone_number = fields.Char(
        related='teacher_id.phone_number', string='phone number')
    plan_time = fields.Boolean(string="time True")

    user_id = fields.Many2one(related='teacher_id.user_id', string="user_id")

    # file
    file_register = fields.Binary(string="file register")

    file_report = fields.Binary(string="file report")
    file_outline = fields.Binary(string="file outline")

    _sql_constraints = [
        ('student_id', 'UNIQUE (student_id)', 'student already exists')]

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['courses'].search([])
        return stage_ids

    @api.constrains('student_id')
    def studentValidate(self):
        for record in self:
            # record.student_id.id same ['student_id','id']
            student_id = record.search_count(
                [('student_id', '=', record.student_id.id)])
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

    @api.model
    def create(self, vals_list):

        # use_in_group_teacher = self.env.user.has_group(
        #     'internship_manager.group_teacher_manager')
        # print("ok>>>>",use_in_group_teacher)
        # if use_in_group_teacher == True:
        #     raise ValidationError(
        #         'Only user belongs to admin are allowed to ....')
        return super().create(vals_list)

    def write(self, vals):
        check_user = self.env.user.has_group(
            'internship_manager.group_department_manager')

        if check_user == False:
            for record in self:
                if record.plan_id:
                    if record.course_id == record.plan_id.course_id:
                        if record.plan_id.type == "edit_topic":
                            start_time = datetime.datetime.combine(
                                record.plan_id.start_time, datetime.time(0, 0))
                            end_time = datetime.datetime.combine(
                                record.plan_id.end_time, datetime.time(23, 59))

                            if start_time < datetime.datetime.now() and end_time > datetime.datetime.now():
                                return super().write(vals)
                            else:
                                raise ValidationError(
                                    "this time is not to update information")
                        else:
                            raise ValidationError(
                                "This course is not scheduled to be updated")
                else:
                    raise ValidationError(
                        "This course is not scheduled to be updated")
        else:
            return super().write(vals)
