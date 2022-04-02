from odoo import fields, models


class Inheriting(models.Model):
    _name = "multiple.inheritance"
    _inherit = ['fleet_management.suppliers', 'fleet_management.countries']
    _description = 'Multiple Inheritance'

    demo = fields.Integer("Demo Field")
