SEARCH_QUERY_MAP = {
    "Desks": "standing office desks ergonomic",

    "Seating": "ergonomic office chairs",

    "Monitors": "computer monitors office",

    "Lighting": "desk lamps led",

    "Storage": "office storage cabinet",

    "Plates & Cups": "disposable plates cups party supplies",

    "Napkins": "party napkins",

    "Decorations": "party decorations balloons",

    "Beverages": "water soda juice",

    "Serving Supplies": "serving trays utensils",

    "Coffee & Tea": "keurig coffee tea",

    "Snacks": "office snack box",

    "Cleaning Supplies": "cleaning wipes sanitizer",

    "Appliances": "mini refrigerator microwave",

    "Conference Tables": "conference meeting tables",

    "Chairs": "conference chairs",

    "Whiteboard": "magnetic whiteboard",

    "Projector": "office projector",

    "Water & Beverages": "water bottles coffee",
}


def generate_search_query(category: str):

    return SEARCH_QUERY_MAP.get(
        category,
        category.lower()
    )