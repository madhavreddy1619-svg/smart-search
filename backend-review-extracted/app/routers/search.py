from fastapi import APIRouter

from app.schemas.search_schema import SearchRequest
from app.services.intent_classifier import classify_intent
from app.services.search_query_generator import generate_search_query
from app.services.ranking_service import rank_products
from app.services.product_service import (
    get_products_by_category,
    search_products_by_keyword,
    search_products_by_brand,
    get_related_products,
)

router = APIRouter()


@router.post("/smart-search")
def smart_search(request: SearchRequest):
    decision = classify_intent(request.query)

    if decision["intent"] == "occasion_goal":
        sections = []

        for category in decision["categories"]:
            products = get_products_by_category(category)

            products = rank_products(
                products,
                group_size=decision["group_size"],
                business_purchase=decision["business_purchase"],
                shopper_type=decision["shopper_type"],
            )

            sections.append({
                "category": category,
                "search_query": generate_search_query(category),
                "products": products,
            })

        return {
            "intent": decision["intent"],
            "query": request.query,
            "cleaned_query": decision["cleaned_query"],
            "group_size": decision["group_size"],
            "shopper_type": decision["shopper_type"],
            "business_purchase": decision["business_purchase"],
            "banner_headline": (
                f"Planning your {decision['goal']} for {decision['group_size']} people?"
                if decision["group_size"]
                else f"Planning your {decision['goal']}?"
            ),
            "banner_subtitle": (
                "Everything sorted by category at the right quantities."
                if decision["group_size"]
                else "Everything sorted by category."
            ),
            "page_type": decision["page_type"],
            "sections": sections,
            "products": [],
        }

    products = []

    if decision["intent"] == "keyword_product":
        products = search_products_by_keyword(decision["cleaned_query"])

    elif decision["intent"] == "brand_lookup":
        products = search_products_by_brand(decision["cleaned_query"])

    elif decision["intent"] == "zero_result_rescue":
        products = search_products_by_keyword(decision["cleaned_query"])

        if len(products) == 0:
            products = get_related_products()

    return {
        "intent": decision["intent"],
        "query": request.query,
        "cleaned_query": decision["cleaned_query"],
        "group_size": decision["group_size"],
        "shopper_type": decision["shopper_type"],
        "business_purchase": decision["business_purchase"],
        "banner_headline": None,
        "banner_subtitle": None,
        "page_type": decision["page_type"],
        "sections": [],
        "products": products,
    }


@router.get("/products")
def get_products(category: str):
    return {
        "category": category,
        "products": get_products_by_category(category),
    }