from schemas.test_plan_model import TestPlanModel


def validate_plan_against_openapi(plan, openapi_paths):
    """
    openapi_paths = openapi["paths"]
    """

    errors = []

    for tc in plan.test_cases:
        path = tc.path
        method = tc.method.lower()

        if path not in openapi_paths:
            errors.append(
                f"{tc.test_name}: path '{path}' not found in OpenAPI"
            )
            continue

        if method not in openapi_paths[path]:
            errors.append(
                f"{tc.test_name}: method '{method.upper()}' not found for path '{path}'"
            )

    if errors:
        raise ValueError("\n".join(errors))
