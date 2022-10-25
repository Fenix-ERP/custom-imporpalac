from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_method = fields.Many2one(
        comodel_name="payment.type",
        string="Payment method",
        ondelete='cascade',
        readonly=True,
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]},
    )
    apply_tax  = fields.Boolean(
        string="Apply Tax", 
        help="Apply tax to the form of payment", 
        default=False
    )
    tax_credit_card = fields.Monetary(
        string="Tax credit card", store=True, readonly=True
    )

    @api.onchange("payment_method")
    def _onchange_payment_method(self):
        if self.payment_method:
            self._amount_all()

    def _amount_all(self):
        res = super()._amount_all()
        for order in self:
            if self.payment_method.apply_tax:
                self.apply_tax = True
                self.tax_credit_card = (
                    self.amount_total * self.payment_method.tax_percentage
                ) / 100
                order.update(
                    {
                        "amount_total": self.amount_total + self.tax_credit_card,
                    }
                )
            else:
                self.tax_credit_card = 0.00
                self.apply_tax = False
        return res


class AccountMove(models.Model):
    _inherit = 'account.move'

    tax_credit_card = fields.Monetary(
        string="Tax credit card", store=True, readonly=True
    )

