from odoo import models, fields


class UpdateCompanyValuation(models.TransientModel):
    _name = 'update.company'
    _description = 'Update Company'

    company_id = fields.Many2one('fleet_management.company', string='Company Name')

    def update_comp_val(self):
        """"
        This method is used to update driver wins
        ------------------------------------------
        :param self: object pointer
        """
        # print(self.company_id.id)
        if self.company_id.id == 1:
            act = self.env.ref('fleet_management.action_mercedes_cars').read()[0]
            # print("MERCEDES")
            # print(act)
            return act



