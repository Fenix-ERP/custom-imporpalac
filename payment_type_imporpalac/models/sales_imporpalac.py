from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_method = fields.Many2one(
        comodel_name="payment.type",
        string="Payment method",
        ondelete="cascade",
        readonly=True,
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]},
    )
    apply_tax = fields.Boolean(
        string="Apply Tax", help="Apply tax to the form of payment", default=False
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
            if order.payment_method.apply_tax:
                order.apply_tax = True
                order.tax_credit_card = (
                    order.amount_total * order.payment_method.tax_percentage
                ) / 100
                order.update(
                    {
                        "amount_total": order.amount_total + order.tax_credit_card,
                    }
                )
            else:
                order.tax_credit_card = 0.00
                order.apply_tax = False
        return res

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals["payment_method"] = self.payment_method
        invoice_vals["apply_tax"] = self.apply_tax
        invoice_vals["tax_credit_card"] = self.tax_credit_card
        return invoice_vals


class AccountMove(models.Model):
    _inherit = "account.move"

    payment_method = fields.Many2one(
        comodel_name="payment.type",
        string="Payment method",
        ondelete="cascade",
        readonly=True,
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]},
    )
    apply_tax = fields.Boolean(
        string="Apply Tax", help="Apply tax to the form of payment", default=False
    )
    tax_credit_card = fields.Monetary(
        string="Tax credit card", store=True, readonly=True
    )

    def _recompute_cash_rounding_lines(self):
        self.ensure_one()
        if self.apply_tax and self.tax_credit_card > 0:
            date = self.date
            currency = self.currency_id
            company = self.company_id
            sign = -1
            amount_currency = self.tax_credit_card * sign
            balance = currency._convert(
                amount_currency,
                company.currency_id,
                company,
                date or fields.Date.context_today(self),
            )
            account = self.payment_method.account_id
            create_method = (
                self.env["account.move.line"].new
                or self.env["account.move.line"].create
            )
            create_method(
                {
                    "name": self.payment_method.name or "",
                    "debit": balance > 0.0 and balance or 0.0,
                    "credit": balance < 0.0 and -balance or 0.0,
                    "quantity": 1.0,
                    "amount_currency": amount_currency,
                    "move_id": self.id,
                    "currency_id": self.currency_id.id,
                    "account_id": account.id,
                    "partner_id": self.commercial_partner_id.id,
                    "exclude_from_invoice_tab": True,
                }
            )
        res = super()._recompute_cash_rounding_lines()
        return res

    def _compute_amount(self):
        res = super()._compute_amount()
        for move in self:
            if move.apply_tax:
                move.update(
                    {
                        "amount_total": move.amount_total + move.tax_credit_card,
                    }
                )
            else:
                move.tax_credit_card = 0.00
                move.apply_tax = False
        return res
