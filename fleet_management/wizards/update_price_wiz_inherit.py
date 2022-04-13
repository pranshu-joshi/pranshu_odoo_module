from odoo import models, fields


# Ex 7 Ques 11
# Ex 7 Ques 12
class UpdatePriceInherited(models.TransientModel):
    _inherit = 'update.price.wiz'

    condition = fields.Selection(
        selection=[('up', 'Up to Date'), ('good', 'Good'), ('avg', 'Average'), ('tbr', 'To be repaired')],
        string='Condition')

    def update_price(self):
        """
        This method is inherited now it can be also used to update condition
        --------------------------------------------------------------------
        :param self: object pointer
        """
        car1 = self.carid
        car1.write({
            'condition': self.condition,
        })
        return super().update_price()
