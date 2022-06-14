from email.policy import default
import re
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class teachers(models.Model):
    _name = 'teachers'
    _description = 'teacher list'
    _rec_name = 'teacher_name'
    # _inherit = 'res.users'

    teacher_name = fields.Char(string='teacher name', required=True)
    teacher_image = fields.Binary(string='teacher image')
    email = fields.Char(string='email', required=True)
    password = fields.Char(string='Password')
    birthday = fields.Date(string='birthday')
    phone_number = fields.Char(string='phone number')
    address = fields.Char(string='address')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', default='male')
    active_email = fields.Boolean(string='Active email')
    active = fields.Boolean(string='Active', default=True)

    teacher_country = fields.Many2one(
        comodel_name='res.country', string='country', store=True, default=241)

    teacher_state = fields.Many2one(
        'res.country.state', string="State", store=True)

    user_id = fields.Many2one(comodel_name='res.users', string='user')

    @api.constrains('user_id')
    def count_users(self):
        if self.user_id:
            for record in self:
                pass

    @api.onchange('user_id')
    def changeUser(self):
        if self.user_id:
            for record in self:
                record.email = record.user_id.email
                record.teacher_name = record.user_id.name
                count_user_def = record.search_count(
                    [('user_id', '=', record.user_id.id)])
                if count_user_def > 0:
                    raise ValidationError(_("Teachers already exist"))
            # return res

    @api.onchange('teacher_country')
    def set_values_to(self):
        if self.teacher_country:
            ids = self.env['res.country.state'].search(
                [('country_id', '=', self.teacher_country.id)])
            return {
                'domain': {'teacher_state': [('id', 'in', ids.ids)], }
            }

    @api.constrains('phone_number')
    def validate_number(self):
        for record in self:
            if record.phone_number:
                if re.findall("[a-zA-Z]", record.phone_number):
                    raise ValidationError('the phone number is not true')
                elif len(record.phone_number) < 10 or len(record.phone_number) >= 11:
                    raise ValidationError('the phone number is wrong')
                else:
                    pass

    @api.model
    def create(self, vals):
        if vals.get('user_id', False):
            user_id = self.env['res.users'].browse(vals.get('user_id', False))
            # vals.update(
            #     {'user_id': user_id.user_id and user_id.user_id.id or False})
        return super(teachers, self).create(vals)

    # @api.constrains('student_name')
    # def cout_student(self):
    #     for record in self:
    #         pass
