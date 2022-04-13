from odoo import fields, models, tools


class CarAnalysis(models.Model):
    _inherit = 'car.analysis'

    condition = fields.Selection(
        selection=[('up', 'Up to Date'), ('good', 'Good'), ('avg', 'Average'), ('tbr', 'To be repaired')],
        string='Condition')

    # com_value = fields.Monetary(currency_field="currency_id", string="Company Valuation")

    def init(self):
        """
        This is an init method which will be used to create a view in postgresql
        ------------------------------------------------------------------------
        :return:
        """
        # The name of the view must respect the name of the model
        # Here if the _name = 'student.analysis'
        # Then the view name should be student_analysis
        # The view must have an id field.
        # This will delete an existing view
        tools.drop_view_if_exists(self._cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW car_analysis AS (
                SELECT fm.id, 
                       ac.name car_name, 
                       ac.company_id, 
                       ac.brand,
                       ac.condition,
                       ac.com_value, 
                       fm.fet_v, 
                       fm.fet_p,
                       fm.sub_fet_v 
                FROM automotives_cars ac, fleet_management_features fm
                WHERE ac.company_id = fm.company_id)""")
