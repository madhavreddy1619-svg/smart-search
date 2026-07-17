def detect_business_purchase(cleaned_query: str, shopper_type: str):
    business_shoppers = ["office_manager", "teacher_or_parent"]

    business_keywords = [
        "office",
        "new hire",
        "break room",
        "conference room",
        "employees",
        "team",
        "bulk",
    ]

    if shopper_type in business_shoppers:
        return True

    for keyword in business_keywords:
        if keyword in cleaned_query:
            return True

    return False