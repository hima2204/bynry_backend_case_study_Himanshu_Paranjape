# Part 2: Database Design

## 1. Schema Design

Based on the requirements, I designed the following schema:

### Company

* id (PK)
* name

### Warehouse

* id (PK)
* company_id (FK)
* name
* location

### Product

* id (PK)
* name
* sku (UNIQUE)
* price (DECIMAL)
* product_type

### Inventory

* id (PK)
* product_id (FK)
* warehouse_id (FK)
* quantity
* UNIQUE(product_id, warehouse_id)

### Inventory_Log

* id (PK)
* product_id
* warehouse_id
* change
* timestamp

### Supplier

* id (PK)
* name
* contact_email

### Product_Supplier

* product_id (FK)
* supplier_id (FK)

### Bundle

* id (PK)
* name

### Bundle_Items

* bundle_id (FK)
* product_id (FK)
* quantity

---

## 2. Missing Requirements / Questions

Some things were not clearly defined, so I would clarify:

* Is SKU unique globally or per company?
* How do we define "recent sales activity"?
* Can a product belong to multiple companies?
* How are bundles priced (sum or custom price)?
* Do we need to track stock transfers between warehouses?
* Should inventory updates be logged for auditing?

---

## 3. Design Decisions

### Unique constraint on inventory

I used a unique constraint on `(product_id, warehouse_id)` to avoid duplicate inventory rows.

---

### Separate inventory log table

This helps track changes over time, which is important for debugging and auditing.

---

### Many-to-many for suppliers

A product can have multiple suppliers, so I used a separate mapping table.

---

### Bundle design

Instead of storing bundle data in product table, I created separate tables to keep it flexible and scalable.

---

## Final Thought

The schema is designed to support multiple warehouses, suppliers, and product types while maintaining data integrity. It can also be extended easily for features like analytics or stock movement tracking.
