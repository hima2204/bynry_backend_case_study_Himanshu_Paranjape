# Part 1: Code Review & Debugging

## 1. Issues Identified

After reviewing the code, I found the following issues:

### Input validation missing

The API directly accesses fields like `data['name']`, `data['sku']`, etc.
If any field is missing, the API will crash instead of returning a proper error.

---

### SKU uniqueness not enforced

There is no check to ensure SKU is unique. This can lead to duplicate products, which can cause confusion in inventory and tracking.

---

### Multiple commits (no transaction handling)

The code commits twice:

* First after creating product
* Then after creating inventory

If the second step fails, the product will exist without inventory, which creates inconsistent data.

---

### No validation of warehouse_id

The code assumes the warehouse exists. If an invalid `warehouse_id` is passed, it may lead to invalid references or errors later.

---

### Inventory duplication issue

A new inventory record is always created. If the same product already exists in the same warehouse, this will create duplicate entries instead of updating quantity.

---

### No error handling

If any database operation fails, there is no rollback or error handling. This can leave the system in a partially updated state.

---

### Price handling is unsafe

Price is taken directly from input. There is no validation for:

* negative values
* incorrect data types

---

### Optional fields not handled

The problem statement mentions some fields might be optional, but the code assumes all fields are present.

---

## 2. Impact in Production

* Duplicate SKUs can break reporting and product identification
* Partial commits can lead to inconsistent data (product without inventory)
* Invalid warehouse IDs can cause data integrity issues
* Duplicate inventory rows can result in incorrect stock calculations
* Lack of validation can allow bad data into the system

Overall, this can reduce trust in the system and create operational issues.

---

## 3. Fixes and Improvements

### Input validation

Check required fields before processing the request and return proper errors if missing.

### Enforce SKU uniqueness

Query the database before inserting to ensure SKU does not already exist.

### Use single transaction

Wrap product and inventory creation in a single transaction so either both succeed or both fail.

### Validate warehouse

Check if the warehouse exists before creating product/inventory.

### Handle inventory properly

If inventory already exists for a product in a warehouse, update quantity instead of creating a new row.

### Add error handling

Use try-except and rollback in case of failure.

### Validate price

Ensure price is numeric and non-negative.

---

## Final Thought

The main issue in the current code is not syntax but lack of production level thinking like validation, transactions, and data integrity. Fixing these makes the API more reliable and safe.
