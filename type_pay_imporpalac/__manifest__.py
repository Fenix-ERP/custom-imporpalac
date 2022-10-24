{
    "name": "Type pay Imporpalac",
    "category": "Sales/Sales",
    "version": "14.0.1.0.0",
    "author": "Bryan Sandoval",
    "company": "Bryan Sandoval / SODI CORP SAS",
    "website": "https://github.com/Fenix-ERP/custom-imporpalac",
    "summary": "This module allows to add the type of payment in the quote",
    "depends": ["sale", "account"],
    "data": [
        "views/sale_views_inherit.xml",
        "views/res_config_settings_views.xml",
        "views/type_payment_view.xml",
        "security/ir.model.access.csv",
        "views/type_payment_menuitem.xml",
    ],
    "demo": [],
    "license": "AGPL-3",
}
