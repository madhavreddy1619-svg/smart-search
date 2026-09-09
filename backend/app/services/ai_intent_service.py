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
    "teacher_or_parent",
    "remote_worker",
    "event_organizer",
    "general_consumer",
    "unknown",
}


SHOPPER_TYPE_ALIASES = {
    "teacher_parent": "teacher_or_parent",
}


GOAL_ALIASES = {
    "home office": "home office",
    "home office setup": "home office",
    "work from home setup": "home office",

    "party": "party",
    "party supplies": "party",
    "event supplies": "party",

    "new hire desk setup": "new hire desk setup",
    "employee desk setup": "new hire desk setup",

    "break room": "break room",
    "break room setup": "break room",
    "break room stocking": "break room",

    "classroom setup": "classroom setup",

    "back to school": "back to school",
    "school supplies": "back to school",

    "conference room setup": "conference room setup",
    "meeting room setup": "conference room setup",

    "tax form organization": "tax forms organization",
    "tax forms organization": "tax forms organization",

    "coffee setup for the office": "coffee setup for the office",
    "office coffee setup": "coffee setup for the office",
}


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing from the environment."
        )

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


def _normalize_goal(goal: Any) -> str | None:
    if not isinstance(goal, str):
        return None

    normalized = goal.strip().lower()

    if not normalized:
        return None

    return GOAL_ALIASES.get(normalized, normalized)


def _normalize_shopper_type(shopper_type: Any) -> str:
    if not isinstance(shopper_type, str):
        return "unknown"

    normalized = shopper_type.strip().lower()

    normalized = SHOPPER_TYPE_ALIASES.get(
        normalized,
        normalized,
    )

    if normalized not in ALLOWED_SHOPPER_TYPES:
        return "unknown"

    return normalized


def _validate_result(
    result: dict[str, Any],
) -> dict[str, Any]:
    intent = result.get(
        "intent",
        "zero_result_rescue",
    )

    if intent not in ALLOWED_INTENTS:
        intent = "zero_result_rescue"

    goal = _normalize_goal(
        result.get("goal")
    )

    if intent != "occasion_goal":
        goal = None

    shopper_type = _normalize_shopper_type(
        result.get(
            "shopper_type",
            "unknown",
        )
    )

    business_purchase = result.get(
        "business_purchase",
        False,
    )

    if not isinstance(
        business_purchase,
        bool,
    ):
        business_purchase = False

    group_size = result.get("group_size")

    if (
        isinstance(group_size, str)
        and group_size.isdigit()
    ):
        group_size = int(group_size)

    if (
        not isinstance(group_size, int)
        or group_size <= 0
    ):
        group_size = None

    return {
        "intent": intent,
        "goal": goal,
        "shopper_type": shopper_type,
        "business_purchase": business_purchase,
        "group_size": group_size,
    }


def classify_with_ai(
    query: str,
) -> dict[str, Any]:
    if not query or not query.strip():
        raise ValueError(
            "Query cannot be empty."
        )

    client = _get_client()

    instructions = """
You classify customer shopping searches for a smart product-search system.

Return only one valid JSON object.
Do not use markdown or explanations.

Allowed intent values:
- occasion_goal
- brand_lookup
- keyword_product
- zero_result_rescue

Intent definitions:

occasion_goal:
The customer describes a broader shopping goal, occasion, room setup,
event, business need, school need, organization task, or shopping mission
that may require products from multiple categories.

Examples:
- help me set up a home office
- supplies for a party of 30 people
- stock the break room
- classroom setup
- new hire desk setup for 10
- organize tax forms
- conference room setup
- coffee setup for the office

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
- coffee
- tax forms

zero_result_rescue:
The query is unclear, highly unusual, severely misspelled, unsupported,
or unlikely to directly match available products.

Shopper type must be exactly one of:
- office_manager
- small_business_owner
- teacher_or_parent
- remote_worker
- event_organizer
- general_consumer
- unknown

For occasion_goal, use one of these canonical goal values whenever
the request matches one of these supported shopping scenarios:
- home office
- party
- new hire desk setup
- break room
- classroom setup
- back to school
- conference room setup
- tax forms organization
- coffee setup for the office

Return exactly these fields:

{
  "intent": "one allowed intent",
  "goal": "canonical goal or null",
  "shopper_type": "one allowed shopper type",
  "business_purchase": true or false,
  "group_size": positive integer or null
}

Rules:
- Set goal only when intent is occasion_goal.
- Do not invent a group size.
- Extract group size when the query contains a number of people,
  employees, students, attendees, desks, hires, or similar group context.
- business_purchase should be true for workplace, company, employee,
  office, procurement, or business-related shopping.
- Direct product searches should remain keyword_product rather than being
  forced into a guided occasion search.
"""

    response = client.responses.create(
        model=os.getenv(
            "OPENAI_MODEL",
        "gpt-5.6-luna",
        ),
        instructions=instructions,
        input=f"Classify this shopping query and return the result as JSON only: {query.strip()}",
        text={
            "format": {
                "type": "json_object",
            }
        },
    )

    raw_text = response.output_text

    if not raw_text:
        raise ValueError(
            "The AI returned an empty response."
        )

    cleaned_text = _clean_json_text(
        raw_text
    )

    try:
        result = json.loads(
            cleaned_text
        )
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"The AI returned invalid JSON: {cleaned_text}"
        ) from exc

    if not isinstance(result, dict):
        raise ValueError(
            "The AI response must be a JSON object."
        )

    return _validate_result(result)