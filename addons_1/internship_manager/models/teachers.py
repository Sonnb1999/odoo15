from email.policy import default
import re
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class teachers(models.Model):
    _inherit = "hr.employee"
    
    active_email = fields.Boolean(string='Active email')
    active = fields.Boolean(string='Active', default=True)

    # @api.onchange('teacher_country')
    # def set_values_to(self):
    #     if self.teacher_country:
    #         ids = self.env['res.country.state'].search(
    #             [('country_id', '=', self.teacher_country.id)])
    #         return {
    #             'domain': {'teacher_state': [('id', 'in', ids.ids)], }
    #         }

    # @api.constrains('phone_number')
    # def validate_number(self):
    #     for record in self:
    #         if record.phone_number:
    #             if re.findall("[a-zA-Z]", record.phone_number):
    #                 raise ValidationError('the phone number is not true')
    #             elif len(record.phone_number) < 10 or len(record.phone_number) >= 11:
    #                 raise ValidationError('the phone number is wrong')
    #             else:
    #                 pass

    # @api.model
    # def create(self, vals):
    #     if vals.get('user_id', False):
    #         user_id = self.env['res.users'].browse(vals.get('user_id', False))
    #         # vals.update(
    #         #     {'user_id': user_id.user_id and user_id.user_id.id or False})
    #     return super(teachers, self).create(vals)

    # @api.constrains('student_name')
    # def cout_student(self):
    #     for record in self:
    #         pass
