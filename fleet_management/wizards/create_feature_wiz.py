from odoo import models, fields


class UpdateFeaturesWiz(models.TransientModel):
    _name = 'update.features.wiz'
    _description = 'Update Features Wizard'

    ID = fields.Integer('Feature_id')
    Model = fields.Many2one('automotives.cars', "Model", ondelete="cascade")
    feature_name = fields.Char('Feature')
    fet_v = fields.Float("Feature Version")
    fet_p = fields.Float("Feature Popularity")
    sub_fet_v = fields.Float("Sub Feature Version")

    def update_features(self):
        """
        This method will be used to update the feature which is O2M of the car
        ----------------------------------------------------------------------
        :param self: object pointer
        """

        feature = self.env['fleet_management.features']
        feature.create({
            'ID': self.ID,
            'feature_name': self.feature_name,
            'Model': self.Model.id,
            'fet_v': self.fet_v,
            'fet_p': self.fet_p,
            'sub_fet_v': self.fet_v,
        })

        obj = self.env['automotives.cars']
        obj.write({
            'feature_ids': [0, 0, feature.id]})
