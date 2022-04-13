from odoo import models, fields


class ReportWiz(models.TransientModel):
    _name = 'report.wizard'
    _description = 'Wizard of Report'

    company_id = fields.Many2one('fleet_management.company', 'Company')

    def html_report(self):
        car_obj = self.env['automotives.cars']
        car = car_obj.search([('company_id', '=', self.company_id.id)])
        car_report = self.env.ref('fleet_management.car_report_html')
        data = {
            'form': self.read()[0],
            'docids': car.ids
        }
        return car_report.report_action(car.ids, data=data, config=True)

    def pdf_report(self):
        car_obj = self.env['automotives.cars']
        car = car_obj.search([('company_id', '=', self.company_id.id)])
        car_report = self.env.ref('fleet_management.car_report_pdf')
        data = {
            'form': self.read()[0],
            'docids': car.ids
        }
        return car_report.report_action(car.ids, data=data, config=True)


class ReportWizNew(models.TransientModel):
    _name = 'report.wizard.new'
    _description = 'Alt Wizard Report'

    company_id = fields.Many2one('fleet_management.company', 'Company')

    def html_report(self):
        car_obj = self.env['automotives.cars']
        car = car_obj.search([('company_id', '=', self.company_id.id)])
        car_report = self.env.ref('fleet_management.car_report_html')
        return car_report.report_action(car.ids, data=None, config=True)

    def pdf_report(self):
        car_obj = self.env['automotives.cars']
        car = car_obj.search([('company_id', '=', self.company_id.id)])
        car_report = self.env.ref('fleet_management.car_report_pdf')
        return car_report.report_action(car.ids, data=None, config=True)


# This is the report wizard of overall report

# class OverallReportWiz(models.TransientModel):
#     _name = 'report.overall.wizard'
#     _description = 'Wizard of Overall Report'
#
#     company_id = fields.Many2one('fleet_management.company', 'Company')
#
#     price = fields.Float('Price', digits=(16, 3), help="Car's Price")
#
#     awards = fields.Integer('Awards')
#
#     dom = fields.Date('Date of Manufacture', help="Car's Manufacturing date")
#
#     def html_report(self):
#         car_obj = self.env['automotives.cars']
#         car = car_obj.search([('company_id', '=', self.company_id.id)])
#         car_report = self.env.ref('fleet_management.car_report_html')
#         data = {
#             'form': self.read()[0],
#             'docids': car.ids,
#             'price': self.price,
#             'country_list': self.awards,
#             'dom': self.dom
#         }
#         return car_report.report_action(car.ids, data=data, config=True)
#
#     def pdf_report(self):
#         car_obj = self.env['automotives.cars']
#         car = car_obj.search([('company_id', '=', self.company_id.id)])
#         car_report = self.env.ref('fleet_management.car_report_pdf')
#         data = {
#             'form': self.read()[0],
#             'docids': car.ids,
#             'supplier_list': self.price,
#             'country_list': self.awards,
#             'dom': self.dom
#         }
#         return car_report.report_action(car.ids, data=data, config=True)
