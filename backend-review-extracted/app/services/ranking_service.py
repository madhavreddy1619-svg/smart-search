def rank_products(products, group_size=None, business_purchase=False, shopper_type="unknown"):
    ranked = []

    for product in products:
        score = 0
        name = product["name"].lower()
        category = product["category"].lower()

        if group_size:
            if "bulk" in name or "pack" in name or "bundle" in name or "10 pack" in name:
                score += 10

            if group_size >= 10 and ("100 pack" in name or "10 pack" in name):
                score += 15

            if group_size >= 25 and ("100 pack" in name or "bulk" in name):
                score += 20

        if business_purchase:
            if "office" in name or "conference" in name or "desk" in name:
                score += 8

        if shopper_type == "teacher_or_parent":
            if "classroom" in name or "student" in name:
                score += 8

        if shopper_type == "office_manager":
            if "office" in name or "cabinet" in name:
                score += 6

        ranked.append({
            "score": score,
            "product": product
        })

    ranked.sort(key=lambda item: item["score"], reverse=True)

    return [item["product"] for item in ranked]