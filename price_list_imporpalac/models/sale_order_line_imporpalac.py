from odoo import api, fields, models
from odoo.tools.misc import get_lang


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    pricelist_line_id = fields.Many2one(
        "product.pricelist",
        string="Pricelist Line",
        related="order_id.pricelist_id",
        readonly=True,
    )

    pricelist_line2_id = fields.Many2one(
        "product.pricelist",
        string="Pricelist Line",
    )

    """ Initial value to field taking the value of the reference field. """

    @api.onchange("pricelist_line_id")
    def _onchange_pricelist_line_id(self):
        for record in self:
            if not record.pricelist_line2_id:
                record.pricelist_line2_id = record.pricelist_line_id

    # calculate unit price when price list value is changed
    @api.onchange("pricelist_line2_id", "product_id")
    def _onchange_pricelist_line2_id(self):
        product = self.product_id.with_context(
            lang=get_lang(self.env, self.order_id.partner_id.lang).code,
            partner=self.order_id.partner_id,
            quantity=self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.pricelist_line2_id.id,
            uom=self.product_uom.id,
        )
        self.price_unit = product.price

    # override the method so that it calculates
    # the unit price when the quantity is changed

    @api.onchange("product_uom", "product_uom_qty")
    def product_uom_change(self):
        values = super().product_uom_change()
        self._onchange_pricelist_line2_id()
        return values


class SaleOrder(models.Model):
    _inherit = "sale.order"

    """ when the main price list is changed each order line
    also takes the same value when updating prices is clicked. """

    def update_prices(self):
        for record in self:
            for line in record.order_line:
                line.pricelist_line2_id = record.pricelist_id
        values = super().update_prices()
        return values
