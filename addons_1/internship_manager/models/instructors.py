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

    active_i = fields.Boolean(string='active', default=True)
    email = fields.Char(related='teacher_id.work_email', string='Work email')
    phone_number = fields.Char(
        related='teacher_id.work_phone', string='work phone')
    student_count = fields.Char(
        string='number of student', compute='compute_count_student', store=False)

    student_id = fields.Many2one(
        comodel_name='students', string='student name', required=True, domain="[('instructor_id','=',student_id)]", ondelete='cascade', copy=False)
    student_image = fields.Binary(related='student_id.student_image')
    student_code = fields.Char(
        related='student_id.student_code', string='student code', store=True, default="0")
    birthday = fields.Date(related='student_id.birthday', string='birthday')

    course_id = fields.Many2one(
        related='class_id.course_id', string='course name', store=True, group_expand='_read_group_stage_ids')
    class_id = fields.Many2one(
        related='student_id.class_id', string='class name', store=True)

    department_id = fields.Many2one("hr.department", string="Department")
    teacher_id = fields.Many2one(
        comodel_name='hr.employee', string='teacher name')

    plan_id = fields.One2many(related='course_id.plan_id', string="plans")
    user_id = fields.Many2one(related='teacher_id.user_id', string="User")

    # file
    file_register = fields.Binary(string="file register")
    file_report = fields.Binary(string="file report")
    file_outline = fields.Binary(string="file outline")

    _sql_constraints = [
        ('student_id', 'UNIQUE (student_id)', 'student already exists')]

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        check_user = self.env.user.has_group(
            'internship_manager.group_department_manager')
            
        if check_user == True:
            stage_ids = self.env['courses'].search([])
            return stage_ids
        else:
            stage_ids = self.env['courses'].search(
                [('active_course', '=', 'started')])
            return stage_ids

    # @api.constrains('student_id')
    # def studentValidate(self):
    #     for record in self:
    #         # record.student_id.id same ['student_id','id']
    #         student_id = record.search_count(
    #             [('student_id', '=', record.student_id.id)])
    #         if student_id > 1:
    #             raise ValidationError(_("Student already exists"))

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

    @api.onchange('department_id')
    def set_values_to(self):
        if self.department_id:
            ids = self.env['hr.employee'].search(
                [('department_id', '=', self.department_id.id)])
            return {
                'domain': {'teacher_id': [('id', 'in', ids.ids)], }
            }

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
