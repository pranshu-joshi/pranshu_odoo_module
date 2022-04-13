import base64
import io

import xlsxwriter
from odoo import models, fields


class CarXLSReport(models.TransientModel):
    _inherit = 'car.xls.report.wiz'

    type = fields.Selection([('company', 'Company'),
                             ('condition', 'Condition')], 'Type')
    name = fields.Char(string="Car's Name")
    company_id = fields.Many2one('fleet_management.company', 'Company')
    condition = fields.Selection(
        selection=[('up', 'Up to Date'), ('good', 'Good'), ('avg', 'Average'), ('tbr', 'To be repaired')],
        string='Condition')

    def print_xls_report(self):
        attach_obj = self.env['ir.attachment']
        cars = self.env['automotives.cars']
        dom = []
        if self.type == 'company':
            if self.company_id:
                dom = [('company_id', '=', self.company_id.id)]
        else:
            dom = [('condition', '=', self.condition)]
        if not cars.ids:
            cars = cars.search(dom)

        wb = xlsxwriter.Workbook('car_report.xlsx')
        cell_format = wb.add_format({'bold': True, 'align': 'center'})
        cell_format1 = wb.add_format({'bold': True, 'font_color': 'red', 'align': 'center'})
        for car in cars:
            print(car)
            sheet = wb.add_worksheet(car.name)
            sheet.merge_range(0, 2, 0, 5, car.name + ' Report', cell_format)
            sheet.write(3, 1, 'Name')
            sheet.write(3, 2, car.name)
            sheet.write(4, 1, 'Company', )
            sheet.merge_range(4, 2, 4, 3, car.brand.upper(), cell_format)
            sheet.write(5, 1, 'Price')
            sheet.write(5, 2, car.price)
            sheet.merge_range(8, 1, 8, 4, 'Marks')
            sheet.write(10, 0, 'Feature', cell_format1)
            sheet.write(10, 1, 'Feature Version', cell_format1)
            sheet.write(10, 2, 'Feature Popularity', cell_format1)
            sheet.write(10, 3, 'Sub Feature Version', cell_format1)
            sheet.write(10, 4, 'Overall Feature', cell_format1)
            sheet.write(6, 1, 'Condition', cell_format1)
            sheet.write(6, 2, car.condition, cell_format)
            if car.car_img:
                car_img = io.BytesIO(base64.b64decode(car.car_img))
            sheet.insert_image(3, 6, "image.png", {'image_data': car_img})
            chart = wb.add_chart({'type': 'pie'})

            row = 11
            v_total = 0.0
            total = 0.0
            if cars.feature_id:
                for fet in cars.feature_id:
                    sheet.write(row, 0, fet.feature_name)
                    sheet.write(row, 1, fet.fet_v)
                    sheet.write(row, 2, fet.fet_p)
                    sheet.write(row, 3, fet.sub_fet_v)
                    sheet.write(row, 4, fet.over_fet)
                    v_total += fet.over_fet
                    total = float(fet.fet_v) + float(fet.fet_p) + float(fet.sub_fet_v) + float(fet.over_fet)

                    chart.add_series({
                        'name': [car.name, row-1, 0],
                        'categories': [car.name, row - 1, 1, row - 1, 3],
                        'values': [car.name, row, 1, row, 3],
                    })
                    row += 1
                    sheet.write(row, 0, 'Vertical Total', cell_format)
                    sheet.write(row, 4, v_total, cell_format1)
                    sheet.write(10, 5, 'Horizontal Total', cell_format)
                    sheet.write(row - 1, 5, total, cell_format1)
            sheet.insert_chart('C18', chart)
        wb.close()
        f = open('car_report.xlsx', 'rb')
        xls_data = f.read()
        buf = base64.b64encode(xls_data)
        doc = attach_obj.create({'name': '%s.xlsx' % (cars.company_id.name + ' Report'),
                                 'datas': buf,
                                 'res_model': 'car.xls.report.wiz',
                                 'store_fname': '%s.xlsx' % ('Car Report'),
                                 })
        return {'type': 'ir.actions.act_url',
                'url': 'web/content/%s?download=true' % (doc.id),
                'target': 'current'
                }
