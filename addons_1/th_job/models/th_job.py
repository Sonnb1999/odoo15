from email.policy import default
from operator import index
from odoo import fields, api, models
from odoo.exceptions import ValidationError
import datetime


class th_job(models.Model):
    _name = "th.job.test"
    _description = "th.job.test"
    _rec_name = "th_mission"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    th_start_time = fields.Datetime("Start time", required=True, tracking=True)
    th_end_time = fields.Datetime("End time")

    th_mission = fields.Char("Mission", required=True, tracking=True)
    th_description = fields.Text("Description", required=True, tracking=True)
    th_status = fields.Selection(
        [('new', 'New'), ('in_progress', 'In Progress'),
         ('solved', 'Solved'), ('done', 'Done'),
         ('cancelled', 'Cancelled')], string="Status", required=True, 
         tracking=True, default="new", group_expand='_expand_status')

    th_note = fields.Text('Note', tracking=True)
    th_worker = fields.Many2one(
        comodel_name='res.users', string='Worker', tracking=True)

    _sql_constraints = [
        ('th_mission', 'UNIQUE (th_mission)', 'Mission all already exists')]

    # _sql_constraints = [
    #     ('course_name', 'UNIQUE (course_name)', 'Course all already exists')]

    def _expand_status(self, states, domain, order):
        return [key for key, val in type(self).th_status.selection]

    @api.onchange('th_end_time', 'th_start_time')
    def changeTime(self):
        for record in self:
            if record.th_start_time:
                if record.th_end_time:
                    if record.th_start_time > record.th_end_time:
                        raise ValidationError(
                            "the misson do not start now!: check end time")

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
                    raise ValidationError(
                        "this time is not true: check start time")

    def action_new(self):
        for record in self:
            record.th_status = "new"

    def action_in_progress(self):
        for record in self:
            record.th_status = "in_progress"

    def action_solved(self):
        for record in self:
            record.th_status = "solved"

    def action_done(self):
        for record in self:
            record.th_status = "done"

    def action_cancelled(self):
        for record in self:
            record.th_status = "cancelled"
