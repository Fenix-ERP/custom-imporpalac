{
    "name": "Search Products Imporpalac",
    "category": "Sales/Sales",
    "version": "14.0.1.0.0",
    "author": "Bryan Sandoval",
    "company": "Bryan Sandoval / SODI CORP SAS",
    "website": "https://github.com/Fenix-ERP/custom-imporpalac",
    "summary": """
    Assistant to show the products, their warehouses,
    available quantities and price list if they have one.
    """,
    "depends": ["sale", "price_list_imporpalac"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_views_inherit.xml",
        "wizard/products_wizard_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "demo": [],
    "license": "AGPL-3",
}
