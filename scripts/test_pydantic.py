from tools.openapi_reader import read_openapi
from schemas.test_plan_model import TestPlanModel
from validators.endpoint_validator import validate_plan_against_openapi
from tools.verify_expected_status import verify_expected_status_against_openapi
from tools.openapi_reader import read_openapi
from pathlib import Path
from generators.pytest_generator import generate_pytest

raw_llm_output = """
{
  "endpoint": "/orders",
  "method": "POST",
  "test_cases": [
    {
      "test_name": "create_order_success",
      "description": "valid order",
      "method": "POST",
      "path": "/orders",
      "headers": {
        "Authorization": "Bearer testtoken"
      },
      "query_params": {},
      "path_params": {},
      "body": {
        "item_id": "A1",
        "quantity": 2
      },
      "expected_status": 201,
      "expected_response_contains": {
        "item_id": "A1"
      }
    }
  ]
}
"""
print(raw_llm_output)
plan = TestPlanModel.model_validate_json(raw_llm_output)
openapi = read_openapi("http://127.0.0.1:8000/openapi.json")
errors = verify_expected_status_against_openapi(
    plan,
    openapi["paths"]
)
if errors:
    print("\n".join(errors))
    raise SystemExit("Invalid expected_status in test plan")

print("All expected_status values are valid according to OpenAPI")


endpoints = openapi["paths"]

validate_plan_against_openapi(plan, endpoints)

print("Plan is valid against OpenAPI")

out = Path("generated_tests/test_from_plan.py")
out.parent.mkdir(exist_ok=True)

generate_pytest(plan, out)

print(f"Generated pytest file: {out}")