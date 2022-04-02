from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Automotives(models.Model):
    # _name = 'fleet_management.cars'
    _inherit = 'automotives.cars'

    car_type = fields.Selection(
        selection=[('sedan', 'Sedan'), ('htb', 'Hatchback'), ('suv', 'SUV'), ('muv', 'MUV'), ('lux', 'Luxury'),
                   ('minivan', 'Minivan')], string='Car Type')
    service = fields.Selection(selection=[('basic', 'Basic'), ('std', 'Standard'), ('comp', 'Comprehensive')],
                               string='Services Type')
    kms = fields.Integer('Kilometers Travelled')
    showroom = fields.Many2many(comodel_name='fleet_management.showroom', string='Showrooms')
    notes = fields.Text('Notes')
    state = fields.Selection([('review', "Reviewing"),
                              ('in_repair', "Repairing"),
                              ('test', "Testing"), ('deal', "Dealing"),
                              ('ready', "Ready"), ("sold", "Sold")])
    #
    # country_list = fields.Many2many('fleet_management.countries',
    #                                 'fleet_management_countries_automotives_cars_rel1',
    #                                 'con_id',
    #                                 'car_id',
    #                                 'Countries')

    @api.onchange('brand')
    def onchange_brand(self):
        """
        An Overridden Onchange method to set company Valuation based on brand
        -------------------------------------------
        :param self: object pointer
        """
        super().onchange_brand()
        for car in self:
            if car.brand == 'tata':
                car.priority = str(4)
            elif car.brand == 'bmw':
                car.priority = str(2)
            elif car.brand == 'mercedes':
                car.priority = str(3)

    @api.constrains('email', 'car_type')
    def compare_age(self):
        for car in self:
            if (car.kms > 1000):
                raise ValidationError("Enter Kms")

    # We are inheriting the button's method (Q-7)
    def term_button(self):
        super().term_button()
        print("It is the latest line")


class Showroom(models.Model):
    _name = 'fleet_management.showroom'
    _description = 'Showroom'

    showroom_id = fields.Integer("Showroom's Id")
    name = fields.Char(string="Showroom's City", help='The origin of showroom as per city.')
