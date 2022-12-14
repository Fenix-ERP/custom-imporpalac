{
    "name": "Payment type Imporpalac",
    "category": "Sales/Sales",
    "version": "14.0.1.0.0",
    "author": "Bryan Sandoval",
    "company": "Bryan Sandoval / SODI CORP SAS",
    "website": "https://github.com/Fenix-ERP/custom-imporpalac",
    "summary": "This module allows to add the payment type in the quote",
    "depends": ["sale", "account"],
    "data": [
        "views/sale_views_inherit.xml",
        "views/payment_type_view.xml",
        "security/ir.model.access.csv",
        "views/payment_type_menuitem.xml",
        "views/account_move_views_inherit.xml",
        "report/report_invoice_template.xml",
    ],
    "demo": [],
    "license": "AGPL-3",
}
