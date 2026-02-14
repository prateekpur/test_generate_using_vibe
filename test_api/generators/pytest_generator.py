from pathlib import Path


def generate_pytest(plan, output_file: Path):
    lines = []

    lines.append("import requests")
    lines.append("")
    lines.append("BASE_URL = 'http://127.0.0.1:8000'")
    lines.append("")

    for tc in plan.test_cases:
        fn_name = f"test_{tc.test_name}"

        lines.append(f"def {fn_name}():")
        lines.append(f"    url = BASE_URL + '{tc.path}'")

        # headers
        headers = tc.headers or {}
        lines.append(f"    headers = {headers}")

        # params
        params = tc.query_params or {}
        lines.append(f"    params = {params}")

        # body
        body = tc.body or {}

        method = tc.method.lower()

        if method in ("post", "put", "patch"):
            lines.append(
                f"    resp = requests.{method}(url, json={body}, headers=headers, params=params)"
            )
        else:
            lines.append(
                f"    resp = requests.{method}(url, headers=headers, params=params)"
            )

        lines.append(f"    assert resp.status_code == {tc.expected_status}")

        if tc.expected_response_contains:
            for k, v in tc.expected_response_contains.items():
                lines.append(f"    assert resp.json().get('{k}') == {v!r}")

        lines.append("")

    output_file.write_text("\n".join(lines))
