from odoo import models, fields, api


class SalesDiscount(models.Model):
    _inherit = 'sale.order.line'

    disc_amount = fields.Float("Discount Amount",
                               compute='_calc_disc_amount')

    @api.depends('price_unit', 'discount')
    def _calc_disc_amount(self):
        for amount in self:
            amount.disc_amount = (amount.price_unit * amount.discount) / 100


class InvoiceDiscount(models.Model):
    _inherit = 'account.move.line'

    disc_amount = fields.Float("Discount Amount")

    @api.onchange('discount', 'price_unit')
    def _calc_discount_amount(self):
        for amount in self:
            amount.disc_amount = (amount.price_unit * amount.discount) / 100

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('discount', 0):
                vals.update({
                    'disc_amount': vals['price_unit'] * vals['discount'] / 100.0
                })
        return super(InvoiceDiscount, self).create(vals_list)

    def write(self, vals):
        for line in self:
            if vals.get('discount', 0):
                price_unit = vals.get('price_unit') and vals['price_unit'] or line.price_unit
                vals.update({
                    'disc_amount': price_unit * vals['discount'] / 100.0
                })

        return super().write(vals)