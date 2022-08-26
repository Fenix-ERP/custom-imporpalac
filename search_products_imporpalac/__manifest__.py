{
    "name": "Search Products Imporpalac",
    "summary": """
    Assistant to show the products, their warehouses,
    available quantities and price list if they have one.
    """,
    "author": "Bryan Sandoval",
    "website": "https://github.com/Fenix-ERP/custom-imporpalac",
    "category": "Uncategorized",
    "license": "OPL-1",
    "version": "14.0.1.0.0",
    "depends": ["sale", "price_list_imporpalac"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_views_inherit.xml",
        "wizard/products_wizard_views.xml",
    ],
    "demo": [],
}
