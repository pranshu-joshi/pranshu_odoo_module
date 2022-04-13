from odoo import fields, models


class OverallReportWiz(models.TransientModel):
    _inherit = 'report.overall.wizard'

    condition = fields.Selection(
        selection=[('up', 'Up to Date'), ('good', 'Good'), ('avg', 'Average'), ('tbr', 'To be repaired')],
        string='Condition')

    def html_report(self):
        # inherit = super().html_report()
        # inherit.update({
        #     self.data: {
        #         'condition': self.condition
        #     }
        # })
        # return inherit
        car_obj = self.env['automotives.cars']
        car = car_obj.search([('company_id', '=', self.company_id.id)])
        car_report = self.env.ref('fleet_management.car_report_html')
        data = {
            'form': self.read()[0],
            'docids': car.ids,
            'price': self.price,
            'country_list': self.awards,
            'dom': self.dom,
            'condition': self.condition

        }
        return car_report.report_action(car.ids, data=data, config=True)

    def pdf_report(self):
        # inherit = super().pdf_report()
        # inherit.update({
        #     self.data: {
        #         'condition': self.condition
        #     }
        # })
        # return inherit
        car_obj = self.env['automotives.cars']
        car = car_obj.search([('company_id', '=', self.company_id.id)])
        car_report = self.env.ref('fleet_management.car_report_pdf')
        data = {
            'form': self.read()[0],
            'docids': car.ids,
            'supplier_list': self.price,
            'country_list': self.awards,
            'dom': self.dom,
            'condition': self.condition
        }
        return car_report.report_action(car.ids, data=data, config=True)
