from odoo import fields, models


class InventoryTurnover(models.TransientModel):
    _name = "inventory.turnover"
    _description = "Turnover View"

    name = fields.Char(string="Name", default="Inventory Turnover Report")
    product_ids = fields.Many2many(comodel_name="product.product", string="Product")
    category_id = fields.Many2one(
        comodel_name="product.category", string="Product Category"
    )
    product_option = fields.Selection(
        string="Product",
        selection=[
            ("all", "All"),
            ("product", "By Product"),
            ("category", "By Category"),
        ],
        default="all",
    )
    option_date = fields.Selection(
        string="Date",
        selection=[("all", "All"), ("date", "By date")],
        default="all",
    )
    date_start = fields.Datetime(string="Start Date")
    date_end = fields.Datetime(string="End Date")
    table_turnover = fields.One2many(
        "inventory.turnover.line",
        "inventory_turnover_id",
        "Table",
        readonly=True,
        copy=False,
    )
    option_location = fields.Selection(
        string="Product Location",
        selection=[("all", "All"), ("by_loc", "By Location")],
        default="all",
    )
    view_min_max = fields.Boolean(string="View Min Max", default=False)
    location_id = fields.Many2one(
        "stock.location",
        string="Location",
        domain=[
            ("usage", "=", "internal"),
            ("scrap_location", "=", False),
            ("return_location", "=", False),
        ],
    )
    total_sales_cost = fields.Float(string="Total sales cost")
    total_average_inventory = fields.Float(string=" Total average inventory")
    total_turnover = fields.Float(string="Total turnover")

    # get inventory turnover data
    def search_data(self):
        products = self.search_products()
        lines_move = []
        line_move = {}
        self.total_sales_cost, self.total_average_inventory = 0, 0
        for product in products:
            unit_sales, sales_cost, initial_date, final_date = 0, 0, 0, 0
            records = []
            kardex = self.search_kardex(product.id)
            for index, move in enumerate(kardex.table_kardex):

                if move.type_move == "Output":
                    unit_sales = unit_sales + move.out_qty
                    sales_cost = unit_sales * move.out_cost_uni

                if index == 0:
                    initial_date = move.date_move
                    records.append(move)

                elif index == len(kardex.table_kardex) - 1:
                    final_date = move.date_move
                    records.append(move)

            unit_sales = unit_sales * (-1)
            sales_cost = sales_cost * (-1)

            # average inventory
            if initial_date != 0 and final_date != 0 and kardex.table_kardex:
                for month in range(initial_date.month, final_date.month):
                    record = self.last_move_in_mounth(kardex, month)
                    if record:
                        records.append(record)

            records = set(records)
            average_inventory = self.calculate_average_inventory(records)
            # turnover inventory
            turnover = self.calculate_turnover_inventory(sales_cost, average_inventory)
            current_stock = self.calculate_current_stock(product.id)
            min_quantity, max_quantity = self.calculate_min_max(product.id)
            last_cost = product.standard_price
            self.total_sales_cost += sales_cost
            self.total_average_inventory += average_inventory
            line_move = {
                "product_id": product.id,
                "unit_sales": unit_sales,
                "sales_cost": sales_cost,
                "average_inventory": average_inventory,
                "turnover": turnover,
                "current_stock": current_stock,
                "min_quantity": min_quantity,
                "max_quantity": max_quantity,
                "last_cost": last_cost,
            }
            lines_move.append(self.env["inventory.turnover.line"].create(line_move).id)
        self.write({"table_turnover": [(6, 0, lines_move)]})
        self.total_turnover = (
            self.total_sales_cost / self.total_average_inventory
            if self.total_sales_cost != 0 and self.total_average_inventory != 0
            else 0
        )

    # calculate average inventory
    def calculate_average_inventory(self, moves):
        count, total_amount = 0, 0
        for move in moves:
            total_amount = total_amount + (move.balances * move.ba_cost_uni)
            count += 1
        average_inventory = total_amount / count if count != 0 else 0
        return average_inventory

    # calculate inventory turnover
    def calculate_turnover_inventory(self, sales_cost, average_inventory):
        return (
            sales_cost / average_inventory
            if average_inventory != 0 and sales_cost != 0
            else 0
        )

    # search for the last movement of the kardex that coincides with
    # the month that is passed by parameter
    def last_move_in_mounth(self, kardex, month):
        records = []
        for move in kardex.table_kardex:
            if move.date_move.month == month:
                records.append(move)
        records.sort(key=lambda item: item["date_move"], reverse=True)
        if records:
            return records[0]

    # create an Instance of the kardex to obtain
    # the movements according to the selected options
    def search_kardex(self, prod_id):
        for record in self:
            if record.option_location == "all":
                if record.option_date == "all":
                    kardex = self.env["account.kardex"].create(
                        {
                            "product_id": prod_id,
                        }
                    )
                elif record.option_date == "date":
                    kardex = self.env["account.kardex"].create(
                        {
                            "product_id": prod_id,
                            "date_start": self.date_start,
                            "date_end": self.date_end,
                            "option": "date",
                        }
                    )
            elif record.option_location == "by_loc":
                if record.option_date == "all":
                    kardex = self.env["account.kardex"].create(
                        {
                            "product_id": prod_id,
                            "option_location": "by_loc",
                            "location_id": self.location_id.id,
                        }
                    )
                elif record.option_date == "date":
                    kardex = self.env["account.kardex"].create(
                        {
                            "product_id": prod_id,
                            "date_start": self.date_start,
                            "date_end": self.date_end,
                            "option_location": "by_loc",
                            "location_id": self.location_id.id,
                            "option": "date",
                        }
                    )
            kardex.search_moves()
            return kardex

    # get the products according to the selected filters
    def search_products(self):
        for record in self:
            if record.option_location == "all":
                if record.product_option == "all":
                    return self.env["product.product"].search([])
                elif record.product_option == "category":
                    return self.env["product.product"].search(
                        [("categ_id", "=", self.category_id.id)]
                    )
                elif record.product_option == "product":
                    return self.env["product.product"].search(
                        [("id", "in", self.product_ids.ids)]
                    )
            elif record.option_location == "by_loc":
                products = self.location_id.quant_ids.product_id
                if record.product_option == "all":
                    return self.env["product.product"].search(
                        [("id", "in", products.ids)]
                    )
                elif record.product_option == "category":
                    return self.env["product.product"].search(
                        [
                            ("id", "in", products.ids),
                            ("categ_id", "=", self.category_id.id),
                        ]
                    )
                elif record.product_option == "product":
                    return self.env["product.product"].search(
                        [("id", "in", products.ids), ("id", "in", self.product_ids.ids)]
                    )

    # calculate the current available stock by location
    # or the grouping of all locations.
    def calculate_current_stock(self, prod_id):
        for record in self:
            if record.option_location == "all":
                stock_quant = self.env["stock.quant"].search(
                    [
                        ("product_id", "=", prod_id),
                        ("location_id.usage", "=", "internal"),
                    ]
                )
                available = 0
                for stock in stock_quant:
                    available = available + stock.available_quantity
                return available
            elif record.option_location == "by_loc":
                stock_quant = self.env["stock.quant"].search(
                    [
                        ("product_id", "=", prod_id),
                        ("location_id", "=", record.location_id.id),
                    ]
                )
                return stock_quant.available_quantity

    def calculate_min_max(self, prod_id):
        for record in self:
            if record.option_location == "by_loc":
                record.view_min_max = True
                min_max = self.env["stock.warehouse.orderpoint"].search(
                    [
                        ("product_id", "=", prod_id),
                        ("location_id", "=", record.location_id.id),
                    ]
                )
                return min_max.product_min_qty, min_max.product_max_qty
            else:
                return 0, 0


class InventoryTurnoverLine(models.TransientModel):
    _name = "inventory.turnover.line"
    _description = "Turnover line View"
    _order = "turnover desc"

    inventory_turnover_id = fields.Many2one(
        "inventory.turnover",
        string="Turnover",
        index=True,
        auto_join=True,
        ondelete="cascade",
    )

    product_id = fields.Many2one(
        comodel_name="product.product", string="Product", required=True
    )
    current_stock = fields.Float(string="Current Stock")
    min_quantity = fields.Float(string="Min quantity")
    max_quantity = fields.Float(string="Max quantity")
    last_cost = fields.Float(string="Last cost")
    unit_sales = fields.Float(string="Unit Sales")
    sales_cost = fields.Float(string="Sales cost")
    average_inventory = fields.Float(string="Average Inventory")
    turnover = fields.Float(string="Turnover")
