from odoo import models,fields

class inheritDemo(models.Model):
    _inherit = 'hr.employee'