from datetime import date

from odoo import fields, models, api

cr_dt = date.today()


# This is the main Model (model is always a Class)

class Automotives(models.Model):
    # These are the Attributes of the model
    _name = 'automotives.cars'
    _description = 'Cars'
    _table = 'automotives_cars'
    _order = 'car_id'
    # These attributes are used for the hierarchy of the model (only used when parent and child ids will be given)
    _parent_name = 'parent_id'
    _parent_store = True

    # Here we are giving the Fields of Model.

    car_id = fields.Integer('Car ID', default='')
    name = fields.Char(string="Car's Name", required=True, index=True, size=30, help="Enter Car's Name")
    available = fields.Boolean('Available', default=True, help="Is car available or not")
    price = fields.Float('Price', digits=(16, 3), help="Car's Price")
    dom = fields.Date('Date of Manufacture', required=True, default=cr_dt, index=True, help="Car's Manufacturing date")
    comments = fields.Text('Comments', help="About car")
    template = fields.Html('Template')
    # Here is the selection field where the format will be like List of tuples as below.
    brand = fields.Selection(selection=[('mercedes', 'Mercedes'), ('bmw', 'BMW'), ('tata', 'TATA')], string='Brand')
    onlyfour = fields.Char(string='Unique four char id', size=4)
    active = fields.Boolean('Active', default=True)
    password = fields.Char('Password')
    email = fields.Char('Email')
    url = fields.Char('URL')
    # It will also be as selection field where the stars will be appeared in GUI.
    priority = fields.Selection([(str(ele), str(ele)) for ele in range(5)], 'Ratings')
    sign_in = fields.Float('Sign In')
    sign_out = fields.Float('Sign Out')
    condition = fields.Selection(
        selection=[('up', 'Up to Date'), ('good', 'Good'), ('avg', 'Average'), ('tbr', 'To be repaired')],
        string='Condition')

    # These fields will be used for Amount as well as Currency.
    currency_id = fields.Many2one("res.currency", "Currency")
    com_value = fields.Monetary(currency_field="currency_id", string="Company Valuation")

    # Relational Fields
    company_id = fields.Many2one(comodel_name='fleet_management.company',
                                 string='Company',
                                 ondelete="restrict",
                                 option={"no_create": 1, "no_open": 1})

    # This is One2many field & it will be requiring its inverse's name (which will be Many2many field in its own model)
    # "limit" will be for displaying only specific number of records in GUI
    feature_id = fields.One2many('fleet_management.features',
                                 'Model',
                                 'Model', limit=10)

    supplier_list = fields.Many2many(comodel_name='fleet_management.suppliers',
                                     string='Suppliers')

    # Many2many : In this field the arguments will be as (comodel_name, relation_name, colunmn1, colunmn2, string)
    # In M2m lookup table will be formed which will be giving the matching of ids only (and only contains 2 columns)
    country_list = fields.Many2many('fleet_management.countries',
                                    'fleet_management_countries_automotives_cars_rel',
                                    'con_id',
                                    'car_id',
                                    'Countries')

    # Reference Field will be the combination of Selection and Many2one field
    extra_info = fields.Reference(selection=[('fleet_management.company', '1'), ('fleet_management.features', '2'),
                                             ('fleet_management.suppliers', '3')])

    # Adding Attachment as Binary Field.
    params_store = fields.Binary(string='Car Brochure', attachment=True)
    # This Field is about storing the name of the document file.
    store_fname = fields.Char(string="File Name")
    # For uploading the image.
    car_img = fields.Image(string="Car's Image")
    # Float Fields which are computed on the basis of other fields using compute parameter,
    # and the store field will be used for storing in database.
    total_over_fet = fields.Float(string="Total Overall Feature", compute="_ove_total", store=True)
    total_avg_fet = fields.Float(string="Total Average Feature", compute="_avg_total", store=True)
    total_percent_fet = fields.Integer(string="Total Percentage", compute="_total_percent")
    # This selection will be for Statusbar and default parameter will be for,
    # if any value is not selected then it will be selected.
    state = fields.Selection([('review', "Reviewing"),
                              ('in_repair', "Repairing"),
                              ('test', "Testing"), ('deal', "Dealing"),
                              ('ready', "Ready")], default="review", string="State")
    # This is Sequence Field used for sequencing the records in tree view.
    car_seq = fields.Integer("Cars Seq")

    # It is the method in the module named api.py in Odoo
    @api.depends("feature_id.over_fet")
    def _ove_total(self):
        """
        This method is used for Calculating total of overall feature ratings of all features
        -------------------------------------------------------------------------------------
        @params self : object pointer/record set
        """
        for record in self:
            for i in record.feature_id:
                record.total_over_fet += i.over_fet

    @api.depends("feature_id.avg_fet")
    def _avg_total(self):
        """
        This method is used for Calculating total of overall feature ratings of all features
        -------------------------------------------------------------------------------------
        @params self : object pointer/record set
        """
        for record in self:
            for i in record.feature_id:
                record.total_avg_fet += i.avg_fet

    @api.depends("total_over_fet", "total_avg_fet")
    def _total_percent(self):
        """
        This method is used for Calculating total Percentage feature
        ------------------------------------------------------------
        @params self : object pointer/record set
        """
        for record in self:
            if record.total_over_fet != 0:
                record.total_percent_fet = record.total_avg_fet / record.total_over_fet * 100
            else:
                record.total_percent_fet == 0

    # for giving model hierarchy we use Child and Parent id, which we have to mention in model attributes.
    parent_id = fields.Many2one('automotives.cars', string='Parent Models')
    child_ids = fields.One2many('automotives.cars', 'parent_id', string='Child Models')
    parent_path = fields.Char('Path')


class Company(models.Model):
    _name = 'fleet_management.company'
    _description = 'Company'

    name = fields.Char('Name')
    code = fields.Char('Code')
    company_age = fields.Integer(string="Company's age", group_operator="avg")
    child_ids = fields.One2many('automotives.cars', 'company_id', string="Child Companies")


class Features(models.Model):
    _name = 'fleet_management.features'
    _description = 'Features'
    _rec_name = 'feature_name'

    ID = fields.Integer('Feature_id')
    feature_name = fields.Char('Feature')
    Model = fields.Many2one('automotives.cars', "Model", ondelete="cascade")
    fet_v = fields.Float("Feature Version")
    fet_p = fields.Float("Feature Popularity")
    sub_fet_v = fields.Float("Sub Feature Version")
    over_fet = fields.Float(string="Overall Feature", compute="_overfet")
    avg_fet = fields.Float(string="Average Feature", compute="_avgfet")
    per_fet = fields.Integer(string="Percentage", compute="_percent")

    @api.onchange('fet_v', 'fet_p', 'sub_fet_v')
    def _overfet(self):
        """
        This method is used for Calculating overall feature ratings
        -----------------------------------------------------------
        @params self : object pointer/record set
        """
        for record in self:
            record.over_fet = record.sub_fet_v + record.fet_v + record.fet_p

    @api.onchange('fet_v', 'fet_p', 'sub_fet_v')
    def _avgfet(self):
        """
        This method is used for Calculating average feature ratings
        -----------------------------------------------------------
        @params self : object pointer/record set
        """
        for record in self:
            record.avg_fet = record.fet_v + record.fet_p - record.sub_fet_v

    @api.onchange('avg_fet', 'over_fet')
    def _percent(self):
        """
        This method is used for Calculating percentage feature ratings
        -----------------------------------------------------------
        @params self : object pointer/record set
        """
        for record in self:
            if record.over_fet != 0:
                record.per_fet = record.avg_fet / record.over_fet * 100


class Suppliers(models.Model):
    _name = 'fleet_management.suppliers'
    _description = 'Suppliers'
    _rec_name = 'sup_name'

    sup_id = fields.Integer('Supplier ID')
    sup_name = fields.Char('Supplier Name')
    sup_age = fields.Integer(string="Company's age", group_operator="max")


class Country(models.Model):
    _name = 'fleet_management.countries'
    _description = 'Countries'
    _table = 'fleet_management_countries'
    _rec_name = 'con_name'

    con_id = fields.Integer('Country ID')
    con_name = fields.Char('Country Name')
