from odoo import models,api


class OverallReport(models.AbstractModel):
    _name = 'report.fleet_management.report_overall'
    _description = 'Overall Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("---------------->", data, docids)
        if not docids and data.get('docids', []):
            docids = data['docids']
        print("DDDD", docids)

        docs = self.env['automotives.cars'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': self.env['automotives.cars'],
            'data': data,
            'docs': docs,
            # 'get_overall_fet': self._get_total_overall_fet,
            # 'get_average_fet': self._get_total_average_fet
        }



