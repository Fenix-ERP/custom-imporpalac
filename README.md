
<!-- /!\ Non OCA Context : Set here the badge of your runbot / runboat instance. -->
[![Pre-commit Status](https://github.com/Fenix-ERP/custom-imporpalac/actions/workflows/pre-commit.yml/badge.svg?branch=14.0)](https://github.com/Fenix-ERP/custom-imporpalac/actions/workflows/pre-commit.yml?query=branch%3A14.0)
[![Build Status](https://github.com/Fenix-ERP/custom-imporpalac/actions/workflows/test.yml/badge.svg?branch=14.0)](https://github.com/Fenix-ERP/custom-imporpalac/actions/workflows/test.yml?query=branch%3A14.0)
[![codecov](https://codecov.io/gh/Fenix-ERP/custom-imporpalac/branch/14.0/graph/badge.svg)](https://codecov.io/gh/Fenix-ERP/custom-imporpalac)
<!-- /!\ Non OCA Context : Set here the badge of your translation instance. -->

<!-- /!\ do not modify above this line -->

# Custom modules for Imporpalac

Development of customized modules to solve the commercial flow of Imporpalac

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[inventory_turnover_report](inventory_turnover_report/) | 14.0.1.0.0 |  | Analize inventory turnover
[price_list_imporpalac](price_list_imporpalac/) | 14.0.1.0.0 |  | This module add price list for each order line
[quick_sales](quick_sales/) | 14.0.1.0.0 |  | Quick sales for counter sales
[receipt_product_imporpalac](receipt_product_imporpalac/) | 14.0.1.0.0 |  | Extra column in the receipt of products in which the sale price can be updated
[sales_imporpalac](sales_imporpalac/) | 14.0.1.0.0 |  | This module contains the sales flow that IMPORPALAC requires
[search_products_imporpalac](search_products_imporpalac/) | 14.0.1.0.0 |  | Assistant to show the products, their warehouses, available quantities and price list if they have one.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Fenix ERP
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
