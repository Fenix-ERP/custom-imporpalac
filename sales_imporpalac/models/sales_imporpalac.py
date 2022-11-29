from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_ids = fields.One2many(
        comodel_name="account.payment", inverse_name="sale_order_id", string="Payments"
    )
    payment_count = fields.Integer(
        string="Payments Orders", compute="_compute_payment_ids"
    )
    active_quick_sale = fields.Boolean(
        string="Active quick sales",
        default=lambda self: self.env["ir.config_parameter"]
        .sudo()
        .get_param("sale.active_quick_sale"),
    )

    def action_confirm_pay_order(self):
        # confirm sales order
        self.action_confirm()
        # validate stock
        self.validate_stock()
        # create pay
        self.create_payment()
        return {
            "res_id": self.id,
            "view_mode": "form",
            "res_model": "sale.order",
            "type": "ir.actions.act_window",
            "tag": "reload",
        }

    def validate_stock(self):
        # validate product delivery
        for prod in self.picking_ids:
            for line in prod.move_ids_without_package:
                if line.forecast_availability < line.product_uom_qty:
                    raise UserError(
                        _(
                            "Quantities are not available for product %s",
                            line.product_id.name,
                        )
                    )

    def create_payment(self):
        journal = self.env["account.journal"].search([("type", "=", "cash")], limit=1)
        for order in self:
            self.env["account.payment"].create(
                {
                    "payment_type": "inbound",
                    "partner_type": "customer",
                    "partner_id": order.partner_id.id,
                    "date": order.date_order,
                    "amount": order.amount_total,
                    "journal_id": journal.id,
                    "sale_order_id": self.id,
                }
            )

    @api.depends("payment_ids")
    def _compute_payment_ids(self):
        for order in self:
            order.payment_count = len(order.payment_ids)

    def action_view_payments(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "account.action_account_payments"
        )
        payments = self.mapped("payment_ids")
        if len(payments) > 1:
            action["domain"] = [("id", "in", payments.ids)]
        elif payments:
            form_view = [(self.env.ref("account.view_account_payment_form").id, "form")]
            if "views" in action:
                action["views"] = form_view + [
                    (state, view) for state, view in action["views"] if view != "form"
                ]
            else:
                action["views"] = form_view
            action["res_id"] = payments.id
        return action
