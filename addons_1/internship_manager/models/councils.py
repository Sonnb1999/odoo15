from odoo import api, fields, models
from odoo.exceptions import ValidationError

location_list = [('C5.501', 'C5.501'),
                 ('C5.502', 'C5.502'),
                 ('C5.503', 'C5.503'),
                 ('C5.504', 'C5.504'),
                 ('C5.505', 'C5.505'),
                 ('C5.506', 'C5.506'),
                 ('C5.507', 'C5.507'),
                 ]

exam_forms_list = [('online exam', 'online exam'), (
    'offline exam', 'offline exam')]


class councils(models.Model):
    _name = 'councils'
    _description = 'council list'
    _rec_name = 'course_id'

    teacher_id = fields.Many2one(
        comodel_name='teachers', string='Teacher name', required=True, ondelete='cascade')
    course_id = fields.Many2one(
        comodel_name='courses', string='Course name', required=True, ondelete='cascade') 

    course_start_time = fields.Date(
        related='course_id.start_time', string='Course start time', store=True)

    course_end_time = fields.Date(
        related='course_id.end_time', string='Course end time', store=True)

    exam_forms = fields.Selection(exam_forms_list)
    location = fields.Selection(location_list)

    start_time = fields.Date(string='Start time', required=True)
    end_time = fields.Date(string='End time', required=True)

    # _sql_constraints = [
    #     ('course_id', 'UNIQUE (course_id)', 'The course already exists')]

    @api.constrains('start_time', 'end_time', 'course_start_time', 'course_end_time')
    def time(self):
        for record in self:
            if record.start_time > record.end_time:
                raise ValidationError('start time < end time')
            else:
                if record.course_start_time > record.start_time:
                    raise ValidationError('the course hasn\'t started yet')
                elif record.course_end_time < record.end_time:
                    raise ValidationError('The course has ended')

                elif record.start_time > record.course_end_time:
                    raise ValidationError('the start time is not suitable')

                elif record.end_time < record.course_start_time:
                    raise ValidationError('the end time is not suitable')
