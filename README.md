# test_api

Demo project for API testing with FastAPI + pytest, plus a simple AI-assisted test-plan-to-test-code workflow.

## What this project contains

- A demo API: login + orders endpoints (`demo_api/app.py`)
- Handwritten tests for core and edge scenarios (`tests/`)
- Test plan schema/validation models (`schemas/`, `validators/`, `tools/`)
- A generator that converts a structured test plan into pytest code (`generators/pytest_generator.py`)
- A sample generated test file (`generated_tests/test_from_plan.py`)

## Project structure

```text
test_api/
├── demo_api/
│   └── app.py
├── tests/
│   ├── test_orders_api.py
│   └── test_demo_additional.py
├── agents/
│   └── test_planner_agent.py
├── schemas/
│   ├── test_case_schema.py
│   └── test_plan_model.py
├── generators/
│   └── pytest_generator.py
├── tools/
│   ├── openapi_reader.py
│   └── verify_expected_status.py
├── validators/
│   └── endpoint_validator.py
├── scripts/
│   └── test_pydantic.py
├── specs/
│   └── orders.spec
└── generated_tests/
    └── test_from_plan.py
```

## Prerequisites

- Python 3.10+

## Setup

From inside `test_api/`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn pydantic email-validator requests pytest
```

## Run the demo API

```bash
uvicorn demo_api.app:app --reload
```

Useful URLs:
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## Run tests

Run all tests:

```bash
pytest -q
```

Run only handwritten API tests:

```bash
pytest -q tests/
```

Run generated tests:

```bash
pytest -q generated_tests/
```

## AI-assisted test generation flow

1. Build endpoint test-plan prompts from spec logic (`agents/test_planner_agent.py`).
2. Validate LLM JSON output with Pydantic model (`schemas/test_plan_model.py`).
3. Validate endpoint/status expectations against OpenAPI (`validators/`, `tools/`).
4. Generate pytest code from the validated plan (`generators/pytest_generator.py`).

A local end-to-end sample is in:

```bash
python scripts/test_pydantic.py
```

This script:
- Parses a sample JSON plan,
- Pulls OpenAPI from the running API,
- Validates status codes and endpoint shape,
- Writes tests to `generated_tests/test_from_plan.py`.

## Demo API behavior summary

- `POST /auth/login`
  - Valid creds (`user@test.com` / `secret123`) -> `200` with `access_token`
  - Invalid creds -> `401`
- `POST /orders`
  - Requires `Authorization: Bearer testtoken`
  - Valid body -> `201`
  - Blocked item ID (`BLOCKED`) -> `400`
  - Missing/invalid auth -> `401`
  - Schema violations -> `422`
- `GET /orders/{order_id}`
  - Requires auth
  - Existing order -> `200`
  - Missing order -> `404`

## Notes

- `generated_tests/test_from_plan.py` is generated output and can be overwritten.
- Keep the API server running while executing scripts/tests that call `http://127.0.0.1:8000`.
