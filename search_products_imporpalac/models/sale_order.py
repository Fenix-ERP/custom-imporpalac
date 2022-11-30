from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import get_lang


class SaleOrder(models.Model):
    _inherit = "sale.order"

    active_search_button = fields.Boolean(
        string="Active search button",
        default=lambda self: self.env["ir.config_parameter"]
        .sudo()
        .get_param("sale.active_search_button"),
        compute="_compute_active_search_button",
    )

    def _compute_active_search_button(self):
        for record in self:
            record.active_search_button = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("sale.active_search_button")
            )

    # Open product wizard and query data
    def action_open_wizard(self):
        # clean model product wizard
        self.env["product.wizard"].search([]).unlink()
        # query data
        locations = self.env["stock.location"].search(
            [
                ("usage", "=", "internal"),
                ("scrap_location", "=", False),
                ("return_location", "=", False),
            ]
        )
        show_price_with_vat = (
            self.env["ir.config_parameter"].sudo().get_param("sale.show_price_with_vat")
        )
        for location in locations:
            if location.quant_ids:  # (current stock)
                for stock in location.quant_ids:
                    warehause = self.env["stock.warehouse"].search(
                        [("lot_stock_id", "=", location.id)]
                    )
                    product = self.product_data(stock.product_id)
                    price_unit_with_vat = product.price
                    for tax in product.taxes_id:
                        if "IVA" in tax.name:
                            amount_iva = (tax.amount / 100) * product.price
                            price_unit_with_vat += amount_iva
                        break
                    pricelist_items = self.env["product.pricelist.item"].search(
                        [
                            ("|"),
                            ("|"),
                            ("applied_on", "=", "3_global"),
                            ("product_tmpl_id", "=", product.product_tmpl_id.id),
                            ("product_id", "=", product.id),
                        ]
                    )
                    pricelist = self.env["product.pricelist"].search(
                        [
                            ("|"),
                            ("id", "in", pricelist_items.pricelist_id.ids),
                            ("name", "=", "Public Pricelist"),
                        ]
                    )
                    self.env["product.wizard"].create(
                        {
                            "product_id": product.id,
                            "warehouse_id": warehause.id,
                            "location_id": location.id,
                            "available_quantity": stock.available_quantity,
                            "pricelist_id": self.pricelist_id.id,
                            "price_unit": product.price,
                            "price_unit_with_vat": price_unit_with_vat,
                            "pricelist_domain_ids": [(6, 0, pricelist.ids)],
                            "sale_order_warehouse_id": self.warehouse_id.id,
                            "date_order": self.date_order,
                        }
                    )
        return {
            "name": _("Products"),
            "view_mode": "tree",
            "res_model": "product.wizard",
            "type": "ir.actions.act_window",
            "context": {
                "order_id": self.id,
                "group_by": "product_id",
                "show_price_with_vat": show_price_with_vat,
                "not_show_price_with_vat": not show_price_with_vat,
            },
            "target": "new",
        }

    # define price product
    def product_data(self, product):
        return product.with_context(
            lang=get_lang(self.env, self.partner_id.lang).code,
            partner=self.partner_id,
            quantity=1,
            date=self.date_order,
            pricelist=self.pricelist_id.id,
        )

    # Process data selected in the wizard
    def process_selected_data(self, products):
        order_lines = [(5, 0, 0)]
        # process current order lines
        for current_order_line in self.order_line:
            if current_order_line.product_id:
                data = {
                    "product_id": current_order_line.product_id.id,
                    "product_uom_qty": current_order_line.product_uom_qty,
                    "price_unit": current_order_line.price_unit,
                    "pricelist_line_id": current_order_line.pricelist_line_id.id,
                    "pricelist_line2_id": current_order_line.pricelist_line2_id.id,
                }
            order_lines.append((0, 0, data))
        # process product selected
        for line in products:
            if line.product_id:
                if line.warehouse_id.id == self.warehouse_id.id:
                    data = {
                        "product_id": line.product_id.id,
                        "price_unit": line.price_unit,
                        "pricelist_line_id": line.pricelist_id.id,
                        "pricelist_line2_id": line.pricelist_id.id,
                    }
                else:
                    raise UserError(
                        _(
                            "You are trying to pick a product from a different warehouse "
                            "than the one on the sales order."
                        )
                    )
            order_lines.append((0, 0, data))
        # save data
        self.order_line = order_lines
