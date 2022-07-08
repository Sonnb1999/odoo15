from odoo import fields, api, models


class orentation_class(models.Model):
    _name = "orentation.class"
    _description = "orentation class"
    _rec_name = "orentation_class_name"

    orentation_class_name = fields.Char("Orentation class", required=True)
    code = fields.Char("Code", required=True)
    class_id = fields.Many2one("classes", string="Class name")

    @api.constrains('orentation_class_name')
    def change_text(self):
        for record in self:

            record.code = record.orentation_class_name
