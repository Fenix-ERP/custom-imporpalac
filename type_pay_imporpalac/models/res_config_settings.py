from odoo import api, fields, models


class PayrollConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    tax_credit_card = fields.Float(
        string="Credit card tax", help="Extra fee for credit card payment"
    )

    def set_values(self):
        super(PayrollConfigSettings, self).set_values()
        set_param = self.env["ir.config_parameter"].set_param
        set_param("tax_credit_card", self.tax_credit_card)

    @api.model
    def get_values(self):
        res = super(PayrollConfigSettings, self).get_values()
        get_param = self.env["ir.config_parameter"].sudo().get_param
        res.update(
            tax_credit_card=get_param("tax_credit_card", default=0.00),
        )
        return res
