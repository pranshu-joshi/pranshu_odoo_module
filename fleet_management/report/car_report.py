from odoo import models, api


class FleetCarsReport(models.AbstractModel):
    _name = 'report.fleet_management.report_cars'
    _description = 'Cars Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['automotives.cars'].browse(docids)
        if not docids:
            docids = data['docids']
        return {
            'doc_ids': docids,
            'doc_model': self.env['automotives.cars'],
            'data': data,
            'docs': docs,
            'get_overall_fet': self._get_total_overall_fet,
            'get_average_fet': self._get_total_average_fet
        }

    def _get_total_overall_fet(self, features):
        total = 0.0
        for fet in features:
            total += fet.over_fet
        return total

    def _get_total_average_fet(self, features):
        total = 0.0
        for fet in features:
            total += fet.avg_fet
        return total

