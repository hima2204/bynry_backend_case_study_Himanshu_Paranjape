from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    sku = db.Column(db.String(100), unique=True)
    price = db.Column(db.Float)
    product_type = db.Column(db.String(50))


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
    quantity = db.Column(db.Integer)


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


def get_threshold(product_type):
    # simple assumption
    thresholds = {
        "perishable": 20,
        "electronics": 10,
        "default": 15
    }
    return thresholds.get(product_type, 15)


def has_recent_sales(product_id):
    # placeholder logic
    return True


def estimate_stockout_days(product_id):
    # simple static assumption
    return 5


def get_supplier(product_id):
    # placeholder supplier info
    return {
        "supplier_id": 1,
        "supplier_name": "Default Supplier"
    }


@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):

    try:
        alerts = []

        inventories = db.session.query(Inventory).join(Warehouse).filter(
            Warehouse.company_id == company_id
        ).all()

        for inv in inventories:
            product = Product.query.get(inv.product_id)

            if not product:
                continue

            threshold = get_threshold(product.product_type)

            if inv.quantity < threshold:

                if not has_recent_sales(product.id):
                    continue

                alerts.append({
                    "product_id": product.id,
                    "product_name": product.name,
                    "sku": product.sku,
                    "warehouse_id": inv.warehouse_id,
                    "current_stock": inv.quantity,
                    "threshold": threshold,
                    "days_until_stockout": estimate_stockout_days(product.id),
                    "supplier": get_supplier(product.id)
                })

        return jsonify({
            "alerts": alerts,
            "total_alerts": len(alerts)
        }), 200

    except Exception as e:
        return jsonify({"error": "Something went wrong"}), 500


if __name__ == '__main__':
    app.run(debug=True)
