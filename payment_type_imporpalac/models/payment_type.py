from email.policy import default
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PaymentType(models.Model):
    _name = "payment.type"
    _description = "Payments types in sales"

    name = fields.Char(
        string="Name",
        required=True
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env["res.company"]._company_default_get(),
    )
    apply_tax  = fields.Boolean(
        string="Apply Tax", 
        help="Apply tax to the form of payment", 
        default=False
    )
    tax_percentage = fields.Float(
        string="Tax percentage", 
        default = 0.00,
        help="Extra fee for payment type"
    )
    account_id = fields.Many2one(
        comodel_name="account.account",
        string="Account",
        ondelete='cascade'
    )