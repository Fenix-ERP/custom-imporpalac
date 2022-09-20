from odoo import _, models
from odoo.exceptions import UserError


class QuickSale(models.Model):
    _inherit = "sale.order"

    def action_confirm_quick(self):
        # confirm sales order
        self.action_confirm()
        # create invoice
        self.create_quick_invoice()

    def create_quick_invoice(self):
        # validate product delivery
        for prod in self.picking_ids:
            for line in prod.move_ids_without_package:
                if line.forecast_availability >= line.product_uom_qty:
                    line.quantity_done = line.product_uom_qty
                else:
                    raise UserError(
                        _(
                            "Quantities are not available for product %s",
                            line.product_id.name,
                        )
                    )
            prod.button_validate()
        # create invoice
        self._create_invoices()
