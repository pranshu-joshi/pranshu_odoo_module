from odoo import models, api


class FleetCarsReport(models.AbstractModel):
    _inherit = 'report.fleet_management.report_cars'

    @api.model
    def _get_report_values(self, docids, data=None):
        inherited = super()._get_report_values(docids, data=data)
        inherited.update({
            'total_awards': self.demo,
            'safety': self.demo_new

        })
        return inherited

    def demo(self):
        total = 100
        return total

    def demo_new(self):
        safety = 4.0
        return safety


class OverallReport(models.AbstractModel):
    _inherit = 'report.fleet_management.report_overall'


    @api.model
    def _get_report_values(self, docids, data=None):
        inherited = super()._get_report_values(docids, data=data)
        return inherited

        # docs = self.env['automotives.cars'].browse(docids)
        # if not docids:
        #     docids = data['docids']
        # return {
        #     'doc_ids': docids,
        #     'doc_model': self.env['automotives.cars'],
        #     'data': data,
        #     'docs': docs,
        #     # 'get_overall_fet': self._get_total_overall_fet,
        #     # 'get_average_fet': self._get_total_average_fet
        # }