from odoo import models, fields


class AdhrAndPan(models.Model):
    _inherit = 'hr.employee'

    aadhar_no = fields.Integer('Aadhar Number')
    pan_no = fields.Char('PAN Number')


