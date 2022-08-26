from odoo import _, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    sales_price = fields.Float(
        "Sales Price",
        digits="Product Price",
        help="New Price at which the product is sold to customers.",
    )

    """ Add the record the current selling price of the product """

    def create(self, vals):
        try:
            for index, line in enumerate(vals):
                if vals[index]["origin"][0] == "P":  # origin purchase order
                    producto = self.env["product.product"].search(
                        [("id", "=", line["product_id"])]
                    )
                    vals[index]["sales_price"] = producto.product_tmpl_id.list_price
        except Exception:
            values = super().create(vals)
            return values
        values = super().create(vals)
        return values


class Picking(models.Model):
    _inherit = "stock.picking"

    """ Update the sale price of the product when confirming the delivery order """

    def button_validate(self):
        values = super().button_validate()
        try:
            if self.origin[0] == "P" and values is True:  # origin purchase order
                if self.validate_prices():
                    self.update_prices()
        except Exception:
            return values
        return values

    # Update the sale price when it is different from the original
    def update_prices(self):
        for line in self.move_ids_without_package:
            if line.sales_price != line.product_tmpl_id.list_price:
                val = {}
                val["list_price"] = line.sales_price
                record = self.env["product.template"].search(
                    [("id", "=", line.product_id.product_tmpl_id.id)]
                )  # first search record
                record.write(val)  # update record

    # validate that the sale price is not 0,
    # and that if there is a duplicate product template,
    # the sale price can be the same as the original or all products
    # must have the same new sale price.

    def validate_prices(self):
        move_ids = self.move_ids_without_package
        for index1 in range(len(move_ids)):
            if move_ids[index1].sales_price > 0:
                # validate repeat
                for index2 in range(len(move_ids)):
                    if index1 != index2:
                        if (
                            move_ids[index1].product_tmpl_id.id
                            == move_ids[index2].product_tmpl_id.id
                        ):
                            # original price
                            if (
                                move_ids[index1].sales_price
                                == move_ids[index1].product_tmpl_id.list_price
                                or move_ids[index2].sales_price
                                == move_ids[index1].product_tmpl_id.list_price
                            ):
                                continue
                            else:
                                if (
                                    move_ids[index1].sales_price
                                    != move_ids[index2].sales_price
                                ):
                                    raise UserError(
                                        _(
                                            "There are two different selling prices "
                                            "on the product %s or its variants",
                                            move_ids[index1].product_id.name,
                                        )
                                    )
            else:
                raise UserError(
                    _(
                        "The selling price of the product %s cannot be 0 ",
                        move_ids[index1].product_id.name,
                    )
                )
        return True
