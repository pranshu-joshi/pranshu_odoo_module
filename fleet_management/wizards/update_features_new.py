from odoo import fields, models


# Ex 7 Ques 9
class UpdateFeaturesNew(models.TransientModel):
    _name = 'update.features.new'
    _description = 'Update Features New'

    fea_id = fields.Many2one(comodel_name='fleet_management.features', string='Features')
    con_ids = fields.Many2many(comodel_name='fleet_management.countries', string='Countries')

    def update_features_new(self):
        """
        This method is used to update features through cars
        ---------------------------------------------------
        :param self: object pointer
        """
        for fea in self:
            # If you have a O2M field
            feature = fea.con_ids
            print("Fans----------.", feature)

            if len(self.con_ids) == 1:
                action = {
                    'name': 'Feat 1',
                    'type': 'ir.actions.act_window',
                    'res_model': 'fleet_management.countries',
                    'view_mode': 'form',
                    'res_id': feature.ids[0],
                    'domain': [('id', 'in', feature.id)],
                }
                return action
            else:
                action = {
                    'name': 'Feat 2',
                    'type': 'ir.actions.act_window',
                    'res_model': 'fleet_management.countries',
                    'view_mode': 'tree,form',
                    'domain': [('id', 'in', feature.ids)],
                }
                return action

