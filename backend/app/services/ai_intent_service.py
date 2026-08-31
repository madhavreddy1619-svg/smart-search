import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


ALLOWED_INTENTS = {
    "occasion_goal",
    "brand_lookup",
    "keyword_product",
    "zero_result_rescue",
}

ALLOWED_SHOPPER_TYPES = {
    "office_manager",
    "small_business_owner",
    "teacher_parent",
    "remote_worker",
    "event_organizer",
    "general_consumer",
    "unknown",
}


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing from the environment.")

    return OpenAI(api_key=api_key)


def _clean_json_text(text: str) -> str:
    cleaned = text.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    return cleaned.strip()


def _validate_result(result: dict[str, Any]) -> dict[str, Any]:
    intent = result.get("intent", "zero_result_rescue")

    if intent not in ALLOWED_INTENTS:
        intent = "zero_result_rescue"

    goal = result.get("goal")

    if not isinstance(goal, str) or not goal.strip():
        goal = None
    else:
        goal = goal.strip().lower()

    shopper_type = result.get("shopper_type", "unknown")

    if shopper_type not in ALLOWED_SHOPPER_TYPES:
        shopper_type = "unknown"

    business_purchase = result.get("business_purchase", False)

    if not isinstance(business_purchase, bool):
        business_purchase = False

    group_size = result.get("group_size")

    if isinstance(group_size, str) and group_size.isdigit():
        group_size = int(group_size)

    if not isinstance(group_size, int) or group_size <= 0:
        group_size = None

    return {
        "intent": intent,
        "goal": goal,
        "shopper_type": shopper_type,
        "business_purchase": business_purchase,
        "group_size": group_size,
    }


def classify_with_ai(query: str) -> dict[str, Any]:
    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    client = _get_client()

    instructions = """
You classify customer shopping searches for a smart product-search system.

Return only one valid JSON object. Do not use markdown or explanation.

Allowed intent values:
- occasion_goal
- brand_lookup
- keyword_product
- zero_result_rescue

Intent definitions:

occasion_goal:
The customer describes a broader goal, occasion, room setup, event,
business need, school need, organization task, or shopping mission that
may require multiple product categories.

Examples:
- help me set up a home office
- supplies for a party of 30 people
- stock the break room
- classroom setup
- new hire desk setup for 10
- organize tax forms

brand_lookup:
The query clearly asks for a known brand or a product from a specific brand.

Examples:
- Keurig coffee maker
- HP printer
- Logitech keyboard

keyword_product:
The query asks for a normal product or product type.

Examples:
- ergonomic chair
- wireless mouse
- standing desk

zero_result_rescue:
The query is unclear, highly unusual, severely misspelled, unsupported,
or unlikely to directly match available products.

Shopper type must be one of:
- office_manager
- small_business_owner
- teacher_parent
- remote_worker
- event_organizer
- general_consumer
- unknown

Return exactly these fields:
{
  "intent": "one allowed intent",
  "goal": "short normalized goal or null",
  "shopper_type": "one allowed shopper type",
  "business_purchase": true or false,
  "group_size": positive integer or null
}

Rules:
- Set goal only for occasion_goal.
- Use a short normalized goal such as "home office setup",
  "party supplies", "break room stocking", "classroom setup",
  "conference room setup", "new hire desk setup",
  or "tax form organization".
- Extract group size when the query contains a number of people,
  employees, students, attendees, desks, or hires.
- Do not invent a group size.
- business_purchase should be true for workplace, company, employee,
  office, procurement, or business-related shopping.
"""

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        instructions=instructions,
        input=query.strip(),
        text={
            "format": {
                "type": "json_object",
            }
        },
    )

    raw_text = response.output_text

    if not raw_text:
        raise ValueError("The AI returned an empty response.")

    cleaned_text = _clean_json_text(raw_text)

    try:
        result = json.loads(cleaned_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"The AI returned invalid JSON: {cleaned_text}"
        ) from exc

    if not isinstance(result, dict):
        raise ValueError("The AI response must be a JSON object.")

    return _validate_result(result)