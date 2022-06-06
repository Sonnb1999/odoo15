from lib2to3.pgen2.token import RARROW
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class instructors(models.Model):
    _name = 'instructors'
    _description = 'instructors list'
    _rec_name = 'course_id'
    # _inherit = "instructors"

    student_id = fields.Many2one(
        comodel_name='students', string='student name', required=True)
    student_image = fields.Binary(related='student_id.student_image')
    student_code = fields.Char(
        related='student_id.student_code', string='student code', store=True)
    birthday = fields.Date(related='student_id.birthday', string='birthday')

    class_id = fields.Many2one(
        related='student_id.class_id', string='class name')
    course_id = fields.Many2one(
        related='class_id.course_id', string='course name')

    teacher_id = fields.Many2one(
        comodel_name='teachers', string='teacher name')
    # teacher_name = fields.Char(related='teacher_id.teacher_name',string='teacher name')
    email = fields.Char(related='teacher_id.email', string='email')
    phone_number = fields.Char(
        related='teacher_id.phone_number', string='phone number')

    _sql_constraints = [
        ('student_id', 'UNIQUE (student_id)', 'student already exists')]

    # @api.model
    # def create(self, vals):
    #     vals = [vals, ] if not isinstance(vals, (tuple, list)) else vals
    #     for val in vals:
    #         student_id = val["student_id"]
    #         student_records = self.search([('student_id', '=', student_id)])
    #         if student_records:
    #             raise ValidationError(_("student already exists"))
    #     return super(instructors, self).create(vals)

    @api.constrains('student_id')
    def studentValidate(self):
        for record in self:
            # record.student_id.id same ['student_id','id']
            student_id = record.search_count(
                [('student_id', '=', record.student_id.id)])
            print(student_id)
            if student_id > 1:
                raise ValidationError(_("student already exists"))
