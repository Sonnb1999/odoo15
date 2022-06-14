from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class BatchUpdateTeacherWizard(models.TransientModel):
    _name = "teachers.batchupdate.wizard"
    _description = "Batch update for teachers model"

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', default=False)

    teacher_country = fields.Many2one(
        comodel_name='res.country', string='country', store=True, default=241)

    teacher_state = fields.Many2one(
        'res.country.state', string="State", store=True)

    address = fields.Char(string='address')
    teacher_image = fields.Binary(string='teacher_image')

    def multi_update(self):
        ids = self.env.context['active_ids']  # selected record ids
        teachers = self.env["teachers"].browse(ids)
        new_data = {}

        if self.teacher_image:
            new_data["teacher_image"] = self.teacher_image
        if self.address:
            new_data["address"] = self.address
        if self.gender:
            new_data["gender"] = self.gender
        if self.teacher_country:
            new_data["teacher_country"] = self.teacher_country
        if self.teacher_state:
            new_data["teacher_state"] = self.teacher_state

        teachers.write(new_data)

    @api.onchange('teacher_country')
    def set_values_to(self):
        if self.teacher_country:
            ids = self.env['res.country.state'].search(
                [('country_id', '=', self.teacher_country.id)])
            return {
                'domain': {'teacher_state': [('id', 'in', ids.ids)], }
            }
