from odoo import _, api, fields, models
from odoo.exceptions import UserError


class TypePayment(models.Model):
    _name = "type.payment"
    _description = "Types of payments in sales"

    name = fields.Char(
        string="Name",
        required=True
    )
    description = fields.Text(
        string="Description of payment",
        translate=True
    )
    company_id = fields.Many2one('res.company', string='Company')
    apply_tax_credit_card  = fields.Boolean(string=" Apply Tax credit card", default=False)

