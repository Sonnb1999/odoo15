from odoo import fields, api, models
from odoo.exceptions import ValidationError
import datetime


class th_job(models.Model):
    _name = "th.job.test"
    _description = "th.job.test"
    _rec_name = "th_mission"
    th_start_time = fields.Datetime("Start time", required=True)
    th_end_time = fields.Datetime("End time")

    th_mission = fields.Char("Mission", required=True)
    th_description = fields.Text("Description",required=True)
    th_status = fields.Selection(
        [('have_done', 'Have done'), ('unfinished', 'Unfinished'), ('complete', 'Complete')], required=True)
    th_note = fields.Text('Note')

    th_worker = fields.Many2one(comodel_name='res.users', string='Worker')

    _sql_constraints = [
        ('th_mission', 'UNIQUE (th_mission)', 'Mission all already exists')]

    # _sql_constraints = [
    #     ('course_name', 'UNIQUE (course_name)', 'Course all already exists')]

    @api.onchange('th_end_time','th_start_time')
    def changeTime(self):
        for record in self:
            if record.th_start_time:
                if record.th_end_time:
                    if record.th_start_time > record.th_end_time:
                        raise ValidationError("the misson do not start now!: check end time")

    @api.onchange('th_start_time')
    def check_start_time(self):
        now = datetime.datetime.now()
        for record in self:
            if record.th_start_time:
                start = datetime.datetime.strptime(
                    str(record.th_start_time), "%Y-%m-%d %H:%M:%S")
                if start >= now:
                    pass
                else:
                    raise ValidationError("this time is not true: check start time")
