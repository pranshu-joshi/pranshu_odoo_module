from datetime import date

from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

cr_dt = date.today()


# This is the main Model (model is always a Class)

class Automotives(models.Model):
    # These are the Attributes of the model
    _name = 'automotives.cars'
    _description = 'Cars'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _table = 'automotives_cars'
    _order = 'car_id'
    # These attributes are used for the hierarchy of the model (only used when parent and child ids will be given)
    _parent_name = 'parent_id'
    _parent_store = True
    # SQL constraints which are added to the table (here automotives_cars)
    _sql_constraints = [
        ('unique_car_id', 'unique(car_id)', 'The car id should be unique for every car'),
        ('unique_car', 'unique(name, brand)', 'The car name should be unique for every brand'),
        ('check_car_id', 'check(car_id<10000)', 'The car_id is very large')
    ]

    # Exe-4 ---> Q22

    @api.constrains('email')
    def compare_age(self):
        for car in self:
            if len(car.email) < 4:
                raise ValidationError("Email is too short")

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
    awards = fields.Integer('Awards')
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
                                 ondelete="restrict", tracking=True)
    # domain=[('name', 'ilike', 'a')])

    # This is One2many field & it will be requiring its inverse's name (which will be Many2many field in its own model)
    # "limit" will be for displaying only specific number of records in GUI
    feature_id = fields.One2many('fleet_management.features',
                                 'Model',
                                 'Model', limit=10)

    supplier_list = fields.Many2many(comodel_name='fleet_management.suppliers',
                                     string='Suppliers')
    # domain=[('sup_name', 'ilike', '%year')])

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

    current_user = fields.Many2one("res.users", "Current User")

    # for giving model hierarchy we use Child and Parent id, which we have to mention in model attributes.
    parent_id = fields.Many2one('automotives.cars',
                                string='Parent Models', )

    child_ids = fields.One2many('automotives.cars',
                                'parent_id',
                                string='Child Models')
    parent_path = fields.Char('Path')

    view_comments = fields.Boolean("Comments", default=False)

    count_rec1 = fields.Integer(string='', compute='count_rec')

    new_rec_count = fields.Integer('Features')

    deal_on = fields.Datetime("Deal ON")
    deal_off = fields.Datetime("Deal OFF")

    color = fields.Integer('Color')

    barcode = fields.Char('Barcode')

    def term_button(self):
        """
        This method is used for getting the required results on terminal with the help of button.
        -----------------------------------------------------------------------------------------
        @params self : object pointer/record set
        """
        # It will return a recordset containing all the records
        cars = self.env['automotives.cars'].search([])
        print(cars)
        res1 = self.env.lang
        res2 = self.env.company.name
        res3 = self.env.user.name
        res4 = self.env
        view = self.env.ref('fleet_management.view_cars_form')
        mt_dt = self.get_metadata()
        tata = cars.filtered(lambda r: r.brand == 'tata')
        print("TATA : ", tata)
        mercedes = cars.filtered(lambda r: r.brand == 'mercedes')
        print("Mercedes : ", mercedes)
        bmw = cars.filtered(lambda r: r.brand == 'bmw')
        print("BMW : ", bmw)
        print("\nMeta Data of Pre-defined fields ------>", view)
        print("\n", res1, "\n\n", res2, "\n\n", res3, "\n\n", res4, "\n\n", mt_dt, "\n\n")

        cars_pwd = cars.filtered(lambda r: r.password == False)
        print("Whose Password is not present : ", cars_pwd)

        concatenation = cars.mapped(lambda r: (r.name + '-' + str(r.car_id)))
        print(concatenation)

        name_data = cars.mapped('name')
        print(name_data)

        sort = cars.sorted(lambda r: r.dom, reverse=True)
        print(sort)

        # 24.

        if tata < mercedes:
            print("Tata is the subset of Mercedes")
        if mercedes < tata:
            print("Mercedes is the subset of tata")
        if tata < cars:
            print("Cars is the superset of tata & Tata is the subset of Cars")
        if mercedes < cars:
            print("Cars is the superset of mercedes & Mercedes is the subset of Cars")

        # 25.

        res1 = tata | mercedes
        print("\nUnion : ", res1)

        res2 = cars & bmw
        print("\nIntersection : ", res2)

        res3 = cars - tata
        print("\nSet Difference : ", res3)

        # 34.
        res_search = cars.search([('brand', '=', 'bmw')], offset=1, limit=2)
        print("Offset - 1 & Limit - 2 --->", res_search)

        # 35.
        print("With Search --->", self.search([('brand', '=', 'bmw')], count=True))
        print("Without Search --->", self.search_count([('brand', '=', 'bmw')]))

        # 37.
        print("List of dictionary for records --->",
              self.search_read(domain=[('brand', '=', 'bmw')], fields={'car_id', 'name', 'price'}, offset=1, limit=2))

        # 38.
        print("Fetching all the records --->",
              self.search_read(fields=['car_id', 'name'], order='name'))

        # 39.
        res_cuser = self.env['res.users'].search([('login', '=', 'admin')])
        print("Current User's Recordset --->", res_cuser)

        # 40.
        if self.env.user.id == self.create_uid.id:
            print("Record was created by user: ", self.create_uid)

    # depends is the method in the module named api.py in Odoo
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

    def create_supplier(self):
        """
        This method is used to create new supplier(M2M field) on the button click
        --------------------------------------------------------------
        @ params : object / recordset
        """
        ref = self.env['fleet_management.suppliers']
        vals_list = [
            {
                'sup_id': 6,
                'sup_name': 'Jktyres',
                'sup_age': 50
            }
        ]
        add = ref.create(vals_list)

    def create_feature(self):
        """
        This method is used to create new feature(O2M field) on the button click
        --------------------------------------------------------------
        @ params : object / recordset
        """
        add = self.write({'feature_id': [(0, 0, {
            'ID': 23,
            'feature_name': 'Offroading',
            'Model': 1,
            'fet_v': 1.2,
            'fet_p': 2.5,
            'sub_fet_v': 1.25})]})

    def write_feature(self):
        """
        This method is used to update feature(O2M field) on the button click
        --------------------------------------------------------------------
        @ params : object / recordset
        """
        rec = self.env['fleet_management.suppliers']
        br_rec = rec.browse(3)
        dict = {
            'sup_id': 10,
            'sup_name': 'XYZ'
        }
        updt = br_rec.write(dict)

    def del_feature(self):
        """
        This method is used to delete feature(O2M field) on the button click
        --------------------------------------------------------------------
        @ params : object / recordset
        """
        self.write({'feature_id': [(3, 5)]})

    def unlink_all(self):
        """
        This method is used to delete all the present features (O2M field) on the button click
        ---------------------------------------------------------------------------------------
        @ params : object / recordset
        """
        # recs = self.env['fleet_management.features']
        self.write({'feature_id': [(5, 0, 0)]})

    def link(self):
        """
        This method is used to link the specific features(O2M field) which are given in the list
        on the button click.
        -----------------------------------------------------------------------------------------
        @ params : object / recordset
        """
        self.write({'country_list': [(6, 0, [5, 6])]})

    def cur_user(self):
        """
        This method will help in fetching the current logged in user.
        -------------------------------------------------------------
        @ params : object / recordset
        """
        self.current_user = self.create_uid

    # def count_features(self):
    #     for rec in self:
    #         rec.new_rec_count = 1

    def count_rec(self):
        """
        This method is counting the number of features(O2M) for a particular method.
        ----------------------------------------------------------------------------
        @ params : object / recordset
        """
        obj = self.env['fleet_management.features']
        for rec in self:
            rec.count_rec1 = obj.search_count([('Model', '=', rec.id)])

    # Exe-4 ---> Q2

    @api.model_create_multi
    def create(self, vals):
        """
        This method is overriding the create method, and we are adding a condition
        which is not in the default create method.
        --------------------------------------------------------------------------
        @ params : object / recordset
        @ params : vals - which is a recordset containing a single value.
        """
        for dict in vals:
            if not dict.get('brand', False):
                dict['brand'] = 'bmw'

        res = super().create(vals)
        print("---------------------", res)
        return res

    # Exe-4 ---> Q1

    @api.model_create_multi
    def create(self, vals_list):
        """
        This method is overriding the create method, and we are creating a record
        in another model(suppliers M2M) by using create method.
        --------------------------------------------------------------------------
        @ params : object / recordset
        @ params : vals - which is a recordset containing a single value.
        """
        obj = self.env['fleet_management.suppliers']
        vals = {
            'sup_id': 7,
            'sup_name': 'Ralco',
            'sup_age': 23
        }
        obj.create(vals)
        res = super().create(vals_list)
        print("---------------------", res)
        return res

    # Exe-4 ---> Q3

    @api.model_create_multi
    def create(self, vals_list):
        """
        This method is overriding the create method, and we are updating a record
        in another model(suppliers M2M) by using browse and write method.
        --------------------------------------------------------------------------
        @ params : object / recordset
        @ params : vals - which is a recordset containing a single value.
        """
        obj = self.env['fleet_management.suppliers']
        vals = {
            'sup_id': 7,
            'sup_name': 'Ralco',
            'sup_age': 23
        }
        obj.create(vals)
        res = super().create(vals_list)
        print("---------------------", res)
        record = obj.browse(4)
        record.write({
            'sup_age': 35
        })
        return res

    # Exe-4 ---> Q5

    def copy(self, default=None):
        """
        This method is overriding the create method, and we are updating a duplicate record's
        name by adding (1) after the name.
        --------------------------------------------------------------------------
        @ params : object / recordset
        @ params : vals - which is a recordset containing a single value.
        """
        default = {
            'name': self.name + '(1)'
        }
        res = super().copy(default=default)
        print("OVERRIDDEN COPY METHOD-----", res)
        return res

    # Exe-4 ---> Q7

    def copy(self, default=None):
        default = {
            'state': 'review'
        }
        res = super().copy(default=default)
        print("OVERRIDDEN COPY METHOD-----", res)
        return res

    # Exe-4 ---> Q8

    def unlink(self):

        # students = stud_obj.search([('standard_id', '=', self.id)])
        if self.state != 'review':
            # raise an error
            err = "You can not delete a car as it is ", self.state, " in state"
            raise UserError(err)
        else:
            return super().unlink()

    # Exe-4 ---> Q13

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     # print(":::::::::::::::::CALLED")
    #     res = super(Automotives, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=False)
    #     print("VIEW TYPE ----->", view_type)
    #     print(res)
    #     if view_type == 'form':
    #         print(">>>>>>>>sortable>>>>>>>>", res.get('fields').get('state').get('sortable'))
    #         k = res.get('fields').get('state').update({'sortable': False})
    #     elif view_type == 'tree':
    #         print(">>>>>>>>sortable>>>>>>>>", res.get('fields').get('state').get('sortable'))
    #         k = res.get('fields').get('state').update({'sortable': False})
    #     return res

    # Exe-4 ---> Q14

    # @api.model
    # def fields_view_get(self, view_id=None,
    #                     view_type='form', toolbar=False, submenu=False):
    #     print("VIEW ID", view_id)
    #     print("VIEW TYPE", view_type)
    #     print("TOOLBAR", toolbar)
    #     res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     if view_type == 'form' or view_type == 'tree':
    #         doc = etree.XML(res['arch'])
    #         ref = doc.xpath("//field[@name='sign_in']")
    #         if ref:
    #             ref[0].set("widget", "float_time")
    #         res['arch'] = etree.tostring(doc, encoding='unicode')
    #     print("RES", res)
    #     return res

    # Exe-4 ---> Q12

    @api.model
    def default_get(self, fields_list):
        print("FIELDS", fields_list)
        res = super().default_get(fields_list)
        res.update({
            'email': 'xyz@gmail.com'
        })
        print("RES", res)
        # seq_obj = self.env['ir.sequence']
        # my_seq = seq_obj.next_by_code('automotives.cars')
        # print("MySEQ", my_seq)
        # res['car_id'] = my_seq
        # print("RES--------->", res)
        return res

    # Exe-4 ---> Q25

    def button_seq(self):
        for car in self:
            car.car_id = self.env['ir.sequence'].next_by_code('automotives.cars')

    # Exe-4 ---> Q15 & 18

    @api.onchange('brand')
    def onchange_brand(self):
        res = {}
        for car in self:
            if car.brand == 'tata':
                car.com_value = 3000.0
            elif car.brand == 'bmw':
                car.com_value = 2000.0
            elif car.brand == 'mercedes':
                car.com_value = 8000.0
            elif car.brand is False:
                res = {
                    'warning': {
                        'title': 'Warning!',
                        'message': 'You should select a brand!'
                    }
                }
                car.com_value = 0.0
                return res

    # Exe-4 ---> Q16

    @api.onchange('brand', 'condition')
    def onchange_brand_condition(self):
        res = {}
        for car in self:
            if car.brand == 'tata' and car.condition == 'up':
                car.awards = 5
            elif car.brand == 'bmw' and car.condition == 'up':
                car.awards = 2
            elif car.brand == 'mercedes' and car.condition == 'up':
                car.awards = 8
            else:
                car.awards = 0.0
        return res

    # Exe-4 ---> Q17

    @api.onchange('company_id')
    def onchange_company(self):

        lst = []
        if self.company_id:
            lst = [('company_id', '=', self.company_id.id)]
        res = {
            'domain': {
                'supplier_list': lst
            }
        }
        return res

    # Exe - 7 Q - 7
    def update_features_new(self):
        """
        This method is used to Update features by directly calling the action
        --------------------------------------------------------------------------
        :param self: object pointer
        """
        act = self.env.ref('fleet_management.action_update_feature_wiz').read()[0]
        return act




class Company(models.Model):
    _name = 'fleet_management.company'
    _description = 'Company'

    name = fields.Char('Name')
    code = fields.Char('Code')
    company_age = fields.Integer(string="Company's age", group_operator="avg")
    child_ids = fields.One2many('automotives.cars', 'company_id', string="Child Companies")

    # Exe-4 ---> Q4

    def write(self, vals):
        if vals.get('name', False):
            vals['code'] = (vals.get('name')[:3] + vals.get('name')[-1]).upper()
        res = super().write(vals)
        print("OVERRIDDEN WRITE", res)
        return res

    # Exe-4 ---> Q9

    def name_get(self):
        com_lst = []
        for com in self:
            com_str = ""
            if com.code:
                com_str += "[" + com.code + "] "
            com_str += com.name
            com_lst.append((com.id, com_str))
        return com_lst

    # Exe-4 ---> Q10

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        srch = ['|', ('code', operator, name), ('name', operator, name)]
        if args:
            srch += args
        standards = self.search(srch, limit=limit)
        return standards.name_get()


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
    company_id = fields.Many2one('fleet_management.company', 'Company')

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

    sup_id = fields.Integer('Supplier ID', copy=False)
    sup_name = fields.Char('Supplier Name')
    sup_age = fields.Integer(string="Company's age", group_operator="max")
    company_id = fields.Many2one('fleet_management.company', 'Company')

    # Exe-4 ---> Q6

    def copy(self, default=None):
        default = {
            'sup_id': self.id + 1
        }
        res = super().copy(default=default)
        return res

    # Exe - 7 Q - 8
    def open_tree(self):
        """
        This method is used to Open Tree view of records by directly calling the action
        -------------------------------------------------------------------------------
        :param self: object pointer
        """
        act = self.env.ref('fleet_management.action_suppliers').read()[0]
        return act


class Country(models.Model):
    _name = 'fleet_management.countries'
    _description = 'Countries'
    _table = 'fleet_management_countries'
    _rec_name = 'con_name'

    con_id = fields.Integer('Country ID')
    con_name = fields.Char('Country Name')
    con_code = fields.Char('Country Code')

    # Exe-4 ---> Q11

    @api.model
    def name_create(self, name):
        if self.con_name > 3:
            vals_lst = [{
                'con_name': name,
                'con_code': name[:3].upper()
            }]
        else:
            vals_lst = [{
                'con_name': name,
                'con_code': name[:2].upper()
            }]
        act = self.create(vals_lst)
        return act.name_get()[0]
