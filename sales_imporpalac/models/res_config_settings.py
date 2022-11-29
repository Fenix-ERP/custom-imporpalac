from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    active_quick_sale = fields.Boolean(
        string="Quick sale",
        help="Activate the quick sales button",
        config_parameter="sale.active_quick_sale",
    )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env["ir.config_parameter"].set_param(
            "sale.active_quick_sale", self.active_quick_sale
        )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res["active_quick_sale"] = (
            self.env["ir.config_parameter"].sudo().get_param("sale.active_quick_sale")
        )
        return res
