from odoo import fields, models
from datetime import date

cr_dt = date.today()

class Automotives(models.Model):
    _name = 'automotives.cars'
    _description = 'Cars'
    _table = 'automotives_cars'
    _order = 'car_id'

    car_id = fields.Integer('Car ID', default='')
    name = fields.Char(string='Name', required=True, index=True, size=30, help="Enter Car's Name")
    available = fields.Boolean('Available', default=True, help="Is car available or not")
    price = fields.Float('Price', digits=(16, 3), help="Car's Price")
    dom = fields.Date('Date of Manufacture', required=True, default=cr_dt, index=True, help="Car's Manufacturing date")
    comments = fields.Text('Comments', help="About car")
    template = fields.Html('Template')
    brand = fields.Selection(selection=[('mercedes', 'Mercedes'), ('bmw', 'BMW'), ('tata', 'TATA')], string='Brand')
    onlyfour = fields.Char(string='Unique four char id', size=4)
    active = fields.Boolean('Active', default=True)
    password = fields.Char('Password')
    email = fields.Char('Email')
    url = fields.Char('URL')
    priority = fields.Selection([(str(ele), str(ele)) for ele in range(5)], 'Ratings')
    sign_in = fields.Float('Sign In')
    sign_out = fields.Float('Sign Out')
    condition = fields.Selection(selection=[('up', 'Up to Date'), ('good', 'Good'), ('avg', 'Average'), ('tbr', 'To be repaired')], string='Condition')

    # Relational Fields
    cars = fields.Many2one(comodel_name='fleet.company', string='company')


class Company(models.Model):
    _name = 'fleet.company'
    _description = 'Company'

    name = fields.Char('Name')
    code = fields.Char('Code')
