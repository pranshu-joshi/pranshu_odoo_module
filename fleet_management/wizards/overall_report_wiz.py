from odoo import models, fields


class OverallReportWiz(models.TransientModel):
    _name = 'report.overall.wizard'
    _description = 'Wizard of Overall Report'

    company_id = fields.Many2one('fleet_management.company', 'Company')

    price = fields.Float('Price', digits=(16, 3), help="Car's Price")

    awards = fields.Integer('Awards')

    dom = fields.Date('Date of Manufacture', help="Car's Manufacturing date")

    def html_report_overall(self):
        car_obj = self.env['automotives.cars']
        car = car_obj.search([('company_id', '=', self.company_id.id)])
        car_report = self.env.ref('fleet_management.overall_report_html')
        print('-------------------------->', car)
        data = {
            'form': self.read()[0],
            'docids': car.ids,
            'price': self.price,
            'country_list': self.awards,
            'dom': self.dom
        }
        return car_report.report_action(car.ids, data=data, config=True)

    def pdf_report_overall(self):
        car_obj = self.env['automotives.cars']
        car = car_obj.search([('company_id', '=', self.company_id.id)])
        car_report = self.env.ref('fleet_management.overall_report_pdf')
        data = {
            'form': self.read()[0],
            'docids': car.ids,
            'supplier_list': self.price,
            'country_list': self.awards,
            'dom': self.dom
        }
        print("--------------------> ", data['docids'])
        return car_report.report_action(car.ids, data=data, config=True)
