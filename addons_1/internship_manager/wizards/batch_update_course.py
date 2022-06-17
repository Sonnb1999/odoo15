from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

Type_of_education = [('formal_university', 'Formal university'),
                     ('affiliated_university', 'Affiliated university')]

Type_of_internship = [('internship', 'Internship'), (
    'professional_practice', 'Professional practice'), ('graduation_thesis', 'Graduation thesis')]


class BatchUpdateCourseWizard(models.TransientModel):
    _name = "courses.batchupdate.wizard"
    _description = "Batch update for courses model"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    educational_system = fields.Selection(
        Type_of_education, string='Type Of Education', default="formal_university")
    type_of_internship = fields.Selection(
        Type_of_internship, string='Type Of Internship', default='professional_practice')

    active_course = fields.Selection([
        ('not_started_yet', 'not started yet'),
        ('started', 'started'),
        ('finished', 'finished'),
    ], string="active course", default='not_started_yet', tracking=True)

    def multi_update(self):
        ids = self.env.context['active_ids']  # selected record ids
        courses = self.env["courses"].browse(ids)
        new_data = {}

        if self.educational_system:
            new_data["educational_system"] = self.educational_system
        if self.type_of_internship:
            new_data["type_of_internship"] = self.type_of_internship
        if self.active_course:
            new_data["active_course"] = self.active_course

        courses.write(new_data)
