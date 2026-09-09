# Smart Search

Smart Search is a full-stack prototype for goal-based e-commerce search.

Traditional product search works well when a customer knows exactly what they want:

```text
ergonomic chair
coffee
tax forms
```

It becomes less useful when the customer searches for a goal instead of a product:

```text
help me setup home office
new hire desk setup for 10
stock the break room
conference room setup for 10
```

Those queries usually require products from several categories. Smart Search identifies that intent and turns the query into a guided set of product recommendations instead of returning one flat list.

The project was built against a Product Requirements Document and validated against the search scenarios defined in that PRD.

---

## What the application does

At a high level, Smart Search decides between two search experiences.

For a direct product query:

```text
ergonomic chair
```

the application keeps the normal search flow and returns matching products.

For a goal-oriented query:

```text
conference room setup for 10
```

the application extracts useful context and builds a guided result:

```text
Conference Tables
Chairs
Whiteboard
Projector
Water & Beverages
```

It can also identify information such as:

* group size
* shopper type
* business purchase context
* relevant product categories
* corrected search text
* whether the page should use standard or guided results

---

## Example

Request:

```http
POST /smart-search
Content-Type: application/json
```

```json
{
  "query": "conference room setup for 10"
}
```

The application identifies the request as a goal-based search:

```json
{
  "intent": "occasion_goal",
  "group_size": 10,
  "shopper_type": "office_manager",
  "business_purchase": true,
  "page_type": "guided_results"
}
```

and returns products grouped into the categories needed for that setup.

A query such as:

```text
coffee
```

takes a different path:

```json
{
  "intent": "keyword_product",
  "page_type": "standard_search"
}
```

No guided experience is added when it is not needed.

---

## Why this project exists

A customer searching for:

```text
new hire desk setup
```

probably needs more than a desk.

They may also need:

* a chair
* a monitor or dock
* keyboard and mouse
* desk supplies
* storage

A basic keyword search does not understand that relationship.

The goal of this project is to put a small intent-understanding layer in front of product search so the application can decide when the customer needs a product and when they need help completing a larger task.

---

## Architecture

```text
                    React Frontend
                          |
                          v
                    FastAPI API
                          |
                          v
                 Intent Classifier
                          |
             +------------+------------+
             |                         |
             v                         v
      Guided Search              Standard Search
             |                         |
             v                         |
     Category Generation               |
             |                         |
             v                         |
      Query Generation                 |
             |                         |
             +------------+------------+
                          |
                          v
                    Product Service
                          |
                          v
                    Ranking Service
                          |
                          v
                      PostgreSQL
```

The backend is intentionally split into small services rather than putting all search logic inside the API route.

The main responsibilities are:

* **Intent classifier** — determines what kind of search the user is making.
* **Search query generator** — maps categories to useful product-search terms.
* **Product service** — reads product data from PostgreSQL.
* **Ranking service** — adjusts product ordering using context such as group size and purchase type.
* **API router** — coordinates the request and returns the final response.

---

## Supported search behavior

The prototype currently handles four intent types:

```text
occasion_goal
keyword_product
brand_lookup
zero_result_rescue
```

### Goal-based searches

These return guided sections.

Examples:

```text
help me setup home office
supplies for party of 30 people
new hire desk setup for 10
stock the break room
```

### Product searches

These remain standard searches.

Examples:

```text
ergonomic chair
tax forms
coffee
```

Keeping these two flows separate is important. The application should not turn every search into an AI-generated experience.

---

## Query normalization

The intent layer also handles simple query cleanup.

For example:

```text
suppiles for party of 20 ppl
```

is interpreted as:

```text
supplies for party of 20 people
```

The system still extracts:

```text
group_size = 20
```

and builds the expected party-supply categories.

Another example:

```text
set up claasroom for 25 students
```

becomes:

```text
set up classroom for 25 students
```

with the group size and classroom context preserved.

---

## Tech stack

### Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* PostgreSQL
* Psycopg2
* OpenAI API

### Frontend

* React
* Vite
* JavaScript

### Development

* Git
* GitHub
* REST
* OpenAPI / Swagger
* Python virtual environments

---

## Project layout

```text
smart-search-project/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── seed_products.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│
├── .gitignore
└── README.md
```

---

## Running the project locally

### Requirements

You will need:

* Python 3.10+
* PostgreSQL
* Node.js
* npm

### Backend

```bash
cd backend
python -m venv venv
```

On Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside `backend`.

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/smart_search
OPENAI_MODEL=your_openai_model
```

The real `.env` file is excluded from Git and should never be committed.

Seed the development product catalog:

```bash
python seed_products.py
```

Start the API:

```bash
python -m uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

From another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend runs locally through Vite, typically at:

```text
http://localhost:5173
```

---

## API endpoints

### Health check

```http
GET /
```

Response:

```json
{
  "message": "Smart Search API is running"
}
```

### Smart search

```http
POST /smart-search
```

Example body:

```json
{
  "query": "stock the break room"
}
```

### Products by category

```http
GET /products?category=Tech
```

---

## PRD validation

The implementation was tested manually against the acceptance queries defined for the prototype.

The following scenarios passed:

| Query                              | Result                                  |
| ---------------------------------- | --------------------------------------- |
| `help me setup home office`        | Guided home-office search               |
| `supplies for party of 30 people`  | Guided party search with group size     |
| `suppiles for party of 20 ppl`     | Typo recovery and group-size extraction |
| `new hire desk setup`              | Guided new-hire setup                   |
| `new hire desk setup for 10`       | Guided setup with quantity context      |
| `back to school supplies`          | Guided school-supply search             |
| `set up claasroom for 25 students` | Typo recovery and classroom setup       |
| `stock the break room`             | Guided break-room search                |
| `help me organize my tax forms`    | Guided document-organization search     |
| `conference room setup for 10`     | Guided conference-room setup            |
| `ergonomic chair`                  | Standard product search                 |
| `tax forms`                        | Standard product search                 |
| `coffee setup for the office`      | Guided office coffee setup              |
| `coffee`                           | Standard product search                 |

**Result: 14 of 14 acceptance scenarios passed.**

The important part of these tests is not just that products were returned. They verify that the system correctly decides **when to use guided search and when to leave normal product search alone**.

---

## A few design decisions

### Keep direct searches simple

If the customer types:

```text
coffee
```

there is no reason to generate an elaborate shopping journey.

The application returns normal search results.

If they type:

```text
coffee setup for the office
```

there is enough context to build a broader solution.

That distinction is deliberate.

### Keep product data outside the AI response

The AI layer helps understand the request.

Actual product results come from the product service and PostgreSQL database rather than relying on the model to invent catalog items.

### Keep the backend modular

Search classification, database access, ranking, and API routing are separate concerns.

That makes it easier to replace individual components later without rewriting the entire application.

For example, the current product lookup could eventually be replaced by a dedicated search engine or vector retrieval layer without changing the public API.

---

## Current limitations

This is a development prototype, not a production commerce search platform.

The current implementation does not include:

* production catalog integration
* customer purchase-history personalization
* clickstream learning
* production search analytics
* large-scale relevance evaluation
* authentication and authorization
* distributed caching
* production observability
* automated A/B testing
* production deployment infrastructure

The product metrics described in the original requirements, such as reducing bounce rate or increasing items per order, are targets for a real production implementation. This repository does not claim those business outcomes.

---

## What I would build next

If I were taking this beyond the prototype, the next work would be:

1. Move the PRD acceptance cases into automated regression tests.
2. Add semantic/vector retrieval for less exact product matches.
3. Add structured logging and search analytics.
4. Measure ranking quality instead of relying only on fixed test scenarios.
5. Add production deployment and CI/CD.
6. Introduce a larger catalog and load-test the search path.

The first priority would be automated regression tests. Search behavior changes easily when prompts, ranking rules, or catalog data change, so the existing acceptance scenarios should eventually run automatically on every relevant code change.

---

## Status

The current version is a working local prototype.

It demonstrates:

* intent-aware search routing
* goal-based product discovery
* keyword search preservation
* typo normalization
* group-size extraction
* shopper-context extraction
* guided category generation
* context-aware ranking
* PostgreSQL-backed product retrieval
* FastAPI/React integration

All 14 prototype acceptance queries have been validated successfully.
