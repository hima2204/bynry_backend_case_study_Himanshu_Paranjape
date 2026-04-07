# Assumptions

Since some requirements were not fully defined, I made the following assumptions:

* SKU is unique across the platform
* Recent sales activity means sales in the last 30 days
* Each product has at least one primary supplier
* Inventory updates should be atomic (no partial updates)
* Low stock threshold is based on product type
* Bundles are combinations of existing products
* Stockout estimation is based on average daily sales

These assumptions can be adjusted based on actual business requirements.
