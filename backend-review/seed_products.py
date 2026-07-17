from app.database import SessionLocal
from app.models.product_model import Product

PRODUCTS = [
    # Tax forms / filing
    {"name": "File Storage Box", "category": "Filing & Storage", "price": 14.99},
    {"name": "Document Organizer Tray", "category": "Document Organizers", "price": 19.99},
    {"name": "Avery File Folder Labels", "category": "Labels", "price": 7.99},
    {"name": "2 Drawer File Cabinet", "category": "File Cabinets", "price": 89.99},
    {"name": "Heavy Duty Binder", "category": "Binders", "price": 8.99},

    # Classroom
    {"name": "Dry Erase Marker Pack", "category": "Writing Supplies", "price": 11.99},
    {"name": "Classroom Notebooks Bulk Pack", "category": "Notebooks", "price": 24.99},
    {"name": "Classroom Poster Set", "category": "Classroom Decor", "price": 13.99},
    {"name": "Classroom Storage Bins", "category": "Storage", "price": 29.99},
    {"name": "Art Supplies Kit", "category": "Art Supplies", "price": 21.99},

    # Extra bulk party
    {"name": "Disposable Plates 100 Pack", "category": "Plates & Cups", "price": 19.99},
    {"name": "Party Cups 100 Pack", "category": "Plates & Cups", "price": 16.99},
    {"name": "Bulk Napkins 200 Pack", "category": "Napkins", "price": 9.99},
    {"name": "Party Tablecloth Pack", "category": "Decorations", "price": 12.99},
    {"name": "Juice Boxes 40 Pack", "category": "Beverages", "price": 22.99},

    # New hire / tech
    {"name": "Monitor Dock Bundle", "category": "Monitors & Docks", "price": 189.99},
    {"name": "Desk Supply Multi Pack", "category": "Desk Supplies", "price": 29.99},
    {"name": "Keyboard Mouse Combo 10 Pack", "category": "Tech", "price": 249.99},

    # Break room
    {"name": "Paper Plates Bulk Pack", "category": "Plates & Cups", "price": 18.99},
    {"name": "Microwave Oven", "category": "Appliances", "price": 119.99},
    {"name": "Coffee Creamer Variety Pack", "category": "Coffee & Tea", "price": 17.99},
    {"name": "Granola Bar Snack Box", "category": "Snacks", "price": 25.99},

    # Conference room
    {"name": "Conference Table Power Hub", "category": "Conference Tables", "price": 149.99},
    {"name": "Stackable Conference Chairs", "category": "Chairs", "price": 299.99},
    {"name": "Projector Screen", "category": "Projector", "price": 129.99},
]


def seed_products():
    db = SessionLocal()

    try:
        for item in PRODUCTS:
            existing = (
                db.query(Product)
                .filter(Product.name == item["name"])
                .first()
            )

            if not existing:
                product = Product(
                    name=item["name"],
                    category=item["category"],
                    price=item["price"],
                )
                db.add(product)

        db.commit()
        print("Products seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_products()