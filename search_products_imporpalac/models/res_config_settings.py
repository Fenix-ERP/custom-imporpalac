from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    active_search_button = fields.Boolean(
        string="Active search button",
        help="Activate summary view of products and warehouses",
        config_parameter="sale.active_search_button",
    )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env["ir.config_parameter"].set_param(
            "sale.active_search_button", self.active_search_button
        )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res["active_search_button"] = (
            self.env["ir.config_parameter"].sudo().get_param("sale.active_search_button")
        )
        return res
