from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class BatchUpdateStudentWizard(models.TransientModel):
    _name = "students.batchupdate.wizard"
    _description = "Batch update for students model"

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', default=False)
    class_id = fields.Many2one('classes', string='class', default=False)
    address = fields.Char(string='address')
    student_image = fields.Binary(string='student_image')

    def multi_update(self):
        ids = self.env.context['active_ids']  # selected record ids
        students = self.env["students"].browse(ids)
        new_data = {}

        if self.student_image:
            new_data["student_image"] = self.student_image
        if self.address:
            new_data["address"] = self.address
        if self.gender:
            new_data["gender"] = self.gender
        if self.class_id:
            new_data["class_id"] = self.class_id

        students.write(new_data)
