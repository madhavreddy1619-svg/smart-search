from app.database import SessionLocal
from app.models.product_model import Product


def product_to_dict(product):
    return {
        "id": product.id,
        "name": product.name,
        "category": product.category,
        "price": float(product.price),
    }


def get_products_by_category(category: str):
    db = SessionLocal()
    try:
        products = db.query(Product).filter(Product.category.ilike(category)).all()
        return [product_to_dict(product) for product in products]
    finally:
        db.close()

def search_products_by_keyword(query: str):
    db = SessionLocal()

    try:
        words = query.split()

        products = db.query(Product).all()

        matched = []

        for product in products:
            text = f"{product.name} {product.category}".lower()

            if all(word.lower() in text for word in words):
                matched.append(product_to_dict(product))

        return matched

    finally:
        db.close()

def search_products_by_brand(query: str):
    db = SessionLocal()

    try:
        words = query.split()

        products = db.query(Product).all()

        matched = []

        for product in products:
            text = product.name.lower()

            if any(word.lower() in text for word in words):
                matched.append(product_to_dict(product))

        return matched

    finally:
        db.close()


def get_related_products():
    db = SessionLocal()
    try:
        products = (
            db.query(Product)
            .order_by(Product.id)
            .limit(6)
            .all()
        )
        return [product_to_dict(product) for product in products]
    finally:
        db.close()