import json


SYSTEM_PROMPT = """
You are a senior QA automation engineer.

Your task is to generate high-value API test cases for one endpoint.

Rules:
- Generate both positive and negative test cases.
- Cover validation errors, authorization errors and business rule failures when applicable.
- Do NOT generate UI tests.
- Do NOT generate test code.
- Output must strictly follow the provided JSON schema.
- Do not add explanations outside JSON.
"""


def build_test_planner_prompt(endpoint_spec: dict) -> str:
    return f"""
You are given the following API endpoint specification extracted from an OpenAPI file.

Endpoint specification:
{json.dumps(endpoint_spec, indent=2)}

Return a JSON object that follows this schema:

{{
  "endpoint": "string",
  "method": "string",
  "test_cases": [
    {{
      "test_name": "string",
      "description": "string",
      "method": "string",
      "path": "string",
      "headers": {{}},
      "query_params": {{}},
      "path_params": {{}},
      "body": {{}},
      "expected_status": 200,
      "expected_response_contains": {{}}
    }}
  ]
}}

Important:
- headers, query_params and path_params must always be present (use empty object if not used).
- body must be null when there is no request body.
- expected_response_contains must only include fields that are stable and predictable.
- test_name must be unique within this endpoint.
"""


if __name__ == "__main__":
    # Temporary manual input for testing the agent

    endpoint_spec = {
        "path": "/orders",
        "method": "POST",
        "has_auth_header": True,
        "request_body_schema": {
            "item_id": {"type": "string", "minLength": 1},
            "quantity": {"type": "integer", "minimum": 1, "maximum": 10}
        },
        "responses": [201, 400, 401, 422]
    }

    prompt = build_test_planner_prompt(endpoint_spec)

    print("----- SYSTEM PROMPT -----")
    print(SYSTEM_PROMPT)
    print("\n----- USER PROMPT -----")
    print(prompt)
