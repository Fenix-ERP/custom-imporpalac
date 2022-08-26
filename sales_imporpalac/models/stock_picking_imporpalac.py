from odoo import _, fields, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"
    payment_exist = fields.Boolean(
        default=False, string="There is a payment", compute="_compute_payment_exist"
    )

    def _compute_payment_exist(self):
        for stock in self:
            sale_order = self.env["sale.order"].search([("name", "=", stock.origin)])
            self.payment_exist = True if sale_order.payment_ids else False

    def action_confirm_and_invoice(self):
        for stock in self:
            sale_order = self.env["sale.order"].search([("name", "=", stock.origin)])
            payment = self.validate_payment(sale_order)
            if payment:
                self.confirm_delivery(stock)
                self.create_invoice(sale_order, payment)

    # validate payment
    def validate_payment(self, sale_order):
        if sale_order.payment_ids:
            for pay in sale_order.payment_ids:
                if pay.state == "draft":
                    raise UserError(_("The payment has not been confirmed"))
                elif pay.state == "posted":
                    return pay
        else:
            raise UserError(_("No payment found for this customer"))

    # confirm delivery
    def confirm_delivery(self, stock):
        for line in stock.move_ids_without_package:
            if line.forecast_availability < line.product_uom_qty:
                raise UserError(
                    _(
                        "Quantities are not available for product %s",
                        line.product_id.name,
                    )
                )
            if (
                line.forecast_availability == line.product_uom_qty
                and line.quantity_done == 0
            ):
                line.quantity_done = line.product_uom_qty
            elif line.quantity_done != line.product_uom_qty:
                raise UserError(
                    _(
                        "The quantity done does not match the demand quantity form product %s",
                        line.product_id.name,
                    )
                )
        stock.button_validate()

    def create_invoice(self, sale_order, payment):
        # create invoice
        sale_order._create_invoices()
        for invoice in sale_order.invoice_ids:
            # confirm invoice
            invoice.action_post()
            # add payment
            id_move_line = (0,)
            for line in payment.line_ids:
                if line.balance < 0.0:
                    id_move_line = line.id
            invoice.js_assign_outstanding_line(id_move_line)
