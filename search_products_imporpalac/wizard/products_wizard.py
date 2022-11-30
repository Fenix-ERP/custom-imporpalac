from odoo import api, fields, models


class ProductWizard(models.TransientModel):
    _name = "product.wizard"
    _description = "See all Products and warehause"

    product_id = fields.Many2one(
        comodel_name="product.product", string="Product", ondelete="cascade"
    )
    barcode = fields.Char(
        string="Barcode", related="product_id.barcode",
    )
    warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse", string="Warehouse", ondelete="cascade"
    )
    location_id = fields.Many2one(
        comodel_name="stock.location", string="Location", ondelete="cascade"
    )
    available_quantity = fields.Float(
        string="Available Quantity",
        digits="Product Unit of Measure",
        required=True,
        default=0.0,
    )
    pricelist_domain_ids = fields.Many2many(
        comodel_name="product.pricelist", string="Pricelist"
    )
    pricelist_id = fields.Many2one(comodel_name="product.pricelist", string="Pricelist")
    price_unit = fields.Float(
        string="Price",
        required=True,
        digits="Product Price",
        default=0.0,
        group_operator=False,
    )
    show_price_with_vat = fields.Boolean(
        string="Show price with vat",
        default=lambda self: self.env["ir.config_parameter"]
        .sudo()
        .get_param("sale.show_price_with_vat"),
    )
    price_unit_with_vat = fields.Float(
        string="Price with Vat",
        required=True,
        digits="Product Price",
        default=0.0,
        group_operator=False,
    )
    sale_order_warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse",
        string="Sale order Warehouse",
        ondelete="cascade",
    )
    date_order = fields.Datetime(
        string="Order Date",
        required=True,
        default=fields.Datetime.now,
        help="Creation date of draft/sent orders",
    )

    def action_get_data(self):
        order = self.env["sale.order"].search([("id", "=", self._context["order_id"])])
        return order.process_selected_data(self)

    @api.onchange("pricelist_id", "product_id")
    def _onchange_pricelist_id(self):
        product = self.product_id.with_context(
            quantity=1,
            date=self.date_order,
            pricelist=self.pricelist_id.id,
        )
        self.price_unit = product.price
        self.price_unit_with_vat = self.price_unit
        for tax in product.taxes_id:
            if "IVA" in tax.name:
                amount_iva = (tax.amount / 100) * product.price
                self.price_unit_with_vat += amount_iva
            break
