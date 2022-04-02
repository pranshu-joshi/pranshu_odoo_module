from odoo import fields, models


class ExtraCompanies(models.Model):
    _name = 'extra.company'
    _description = 'Extra company'
    _inherits = {'fleet_management.company': 'company_id'}
    _table = 'extra_company'
    _rec_name = 'code'

    code = fields.Char(string='Extra Company Name')
    company_awards = fields.Integer('Awards of Company')
    company_id = fields.Many2one('fleet_management.company',
                                 'Extra Companies', required=True, ondelete='cascade')


class ExtraSuppliers(models.Model):
    _name = 'extra.supplier'
    _description = 'Extra Suppliers'
    _rec_name = 'code'

    code = fields.Char('Substitute part supplier')
    supplier_list = fields.Many2one('fleet_management.suppliers',
                                    'Secondary Supplier',
                                    required=True, ondelete='cascade',
                                    delegate=True)
