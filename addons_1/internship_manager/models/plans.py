import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError

from datetime import timedelta

Send_mail = [('Haven\'t sent mail yet', 'Haven\'t sent mail yet'),
             ('Sent the first notification email',
              'Sent the first notification email'),
             ('Emailed the final notification',
              'Emailed the final notification')
             ]

Type_list = [('Submit a Report', 'Submit a Report'), (
    'Edit topic', 'Edit topic'), ('No announcement yet', 'No announcement yet')]


class plans(models.Model):
    _name = 'plans'
    _description = 'plan list'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'plan_name'

    plan_name = fields.Char(string='Plan name', required=True)
    course_id = fields.Many2one(
        comodel_name='courses', string='Course name', required=True, domain="[('active_course','!=','finished')]")

    course_start_time = fields.Date(
        related='course_id.start_time', string='Course start time', store=True)

    course_end_time = fields.Date(
        related='course_id.end_time', string='Course end time', store=True)

    type = fields.Selection(Type_list)
    send_mail = fields.Selection(Send_mail)
    start_time = fields.Date(string='Start time', required=True)
    end_time = fields.Date(string='End time', required=True)

    list_instructor = fields.One2many(
        related='course_id.instructor_ids', string='list instructor')
    email = fields.Char(string='email', store=False)
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

    # auto send_mail

    @api.onchange('course_id', 'start_time')
    def change_course(self):
        ids = self.env['plans'].search_count(
            [('course_id', '=', self.course_id.id)])
        if self.course_id:
            if ids < 1:
                for record in self:
                    record.start_time = record.course_start_time
                    _start = record.start_time
                    # print('type', type(_start))
                    if record.start_time:
                        record.end_time =  record.start_time + timedelta(days=7)

    def getEmail(self):
        pass

    def sendMail(self):
        pass

    def sendMailvalidate(self):
        dateNow = datetime.datetime.now()
        date_send_mail = dateNow + datetime.timedelta(days=2)

        for record in self:
            if record.type == 'No announcement yet':
                raise ValidationError('ko gui mail')
            else:
                # gui mail dau tien
                if record.send_mail == 'Haven\'t sent mail yet':
                    if date_send_mail == record.start_time:
                        raise ValidationError('se gui mail')
                # gui mail thu 2
                elif record.send_mail == 'Sent the first notification email':
                    if date_send_mail == record.end_time:
                        raise ValidationError('da gui mail 1')
                # da gui both mail
                elif record.send_mail == 'Emailed the final notification':
                    raise ValidationError('da gui mail 2')
