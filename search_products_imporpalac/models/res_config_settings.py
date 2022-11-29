from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    active_search_button = fields.Boolean(
        string="Show search product button",
        help="Activate summary view of products and warehouses",
        config_parameter="sale.active_search_button",
    )
    show_price_with_vat = fields.Boolean(
        string="Show sales price with vat",
        help="show the sales price with VAT in the summary view of products and warehouses",
        config_parameter="sale.show_price_with_vat",
    )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env["ir.config_parameter"].set_param(
            "sale.active_search_button", self.active_search_button
        )
        self.env["ir.config_parameter"].set_param(
            "sale.show_price_with_vat", self.show_price_with_vat
        )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res["active_search_button"] = (
            self.env["ir.config_parameter"].sudo().get_param("sale.active_search_button")
        )
        res["show_price_with_vat"] = (
            self.env["ir.config_parameter"].sudo().get_param("sale.show_price_with_vat")
        )
        return res
