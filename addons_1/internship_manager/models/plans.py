from odoo import api, fields, models
from odoo.exceptions import ValidationError

Send_mail = [('haven\'t sent mail yet', 'haven\'t sent mail yet'),
             ('sent the first notification email',
              'sent the first notification email'),
             ('emailed the final notification',
              'emailed the final notification')
             ]

Type_list = [('Submit a Report', 'Submit a Report'), (
    'Edit topic', 'Edit topic'), ('No announcement yet', 'No announcement yet')]


class plans(models.Model):
    _name = 'plans'
    _description = 'plan list'
    _rec_name = 'plan_name'

    plan_name = fields.Char(string='Plan name', required=True)
    course_id = fields.Many2one(comodel_name='courses', string='Course name',required=True)

    course_start_time = fields.Date(
        related='course_id.start_time', string='Course start time', store=True)

    course_end_time = fields.Date(
        related='course_id.end_time', string='Course end time', store=True)

    type = fields.Selection(Type_list)
    send_mail = fields.Selection(Send_mail)
    start_time = fields.Date(string='Start time',required=True)
    end_time = fields.Date(string='End time',required=True)

    _sql_constraints = [
        ('plan_name', 'UNIQUE (plan_name)', 'The plan name already exists')]
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
