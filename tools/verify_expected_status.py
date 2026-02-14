def verify_expected_status_against_openapi(plan, openapi_paths):
    """
    plan: TestPlanModel
    openapi_paths: result of read_openapi()["paths"]   OR your extracted paths map
    """

    errors = []

    for tc in plan.test_cases:
        path = tc.path
        method = tc.method.lower()

        if path not in openapi_paths:
            # already validated elsewhere
            continue

        if method not in openapi_paths[path]:
            # already validated elsewhere
            continue

        operation = openapi_paths[path][method]
        responses = operation.get("responses", {})

        # OpenAPI stores response codes as strings
        allowed_statuses = {k for k in responses.keys() if k.isdigit()}

        expected = str(tc.expected_status)

        if expected not in allowed_statuses:
            errors.append(
                f"{tc.test_name}: expected_status {tc.expected_status} "
                f"not declared for {method.upper()} {path}. "
                f"Allowed: {sorted(allowed_statuses)}"
            )

    return errors
