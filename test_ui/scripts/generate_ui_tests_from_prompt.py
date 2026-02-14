import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from generators.ui_pytest_generator import generate_pytest_from_ui_plan
from schemas.ui_test_plan_model import UITestPlanModel


SYSTEM_PROMPT = """
You are a senior QA automation engineer for web UI testing.
Generate a UI test plan from the user's prompt.

Rules:
- Output JSON only (no markdown, no explanation).
- Return 1-5 meaningful test cases.
- Use actions from this exact list:
  goto, click, fill, press, expect_text, expect_title_contains, expect_url_contains, wait_for_selector
- Prefer stable selectors (data-testid, id, role-based selectors).
- Keep steps deterministic and concise.
""".strip()


SCHEMA_TEMPLATE = {
    "app_name": "string",
    "test_cases": [
        {
            "test_name": "string",
            "description": "string",
            "path": "/",
            "steps": [
                {
                    "action": "goto|click|fill|press|expect_text|expect_title_contains|expect_url_contains|wait_for_selector",
                    "selector": "optional string",
                    "value": "optional string",
                    "expected": "optional string",
                    "timeout_ms": 5000,
                }
            ],
        }
    ],
}


def build_user_prompt(user_prompt: str) -> str:
    return (
        "Create a JSON test plan for the following UI testing request.\n\n"
        f"Request:\n{user_prompt}\n\n"
        f"Output schema:\n{json.dumps(SCHEMA_TEMPLATE, indent=2)}\n"
    )


def extract_json(content: str) -> str:
    text = content.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3:
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines).strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object found in model output")

    return text[start:end + 1]


def request_plan_from_model(user_prompt: str) -> str:
    import requests

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required when --plan-file is not provided")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    response = requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(user_prompt)},
            ],
        },
        timeout=60,
    )
    response.raise_for_status()

    payload = response.json()
    return payload["choices"][0]["message"]["content"]


def _extract_target_app(prompt_text: str) -> str:
    match = re.search(r"target app\s*:\s*(\S+)", prompt_text, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "web_app"


def _extract_credentials(text: str) -> tuple[str, str]:
    match = re.search(r"with\s+([a-zA-Z0-9_]+)\s*/\s*([a-zA-Z0-9_]+)", text, flags=re.IGNORECASE)
    if match:
        return match.group(1), match.group(2)
    return "standard_user", "secret_sauce"


def _extract_numbered_requests(prompt_text: str) -> list[str]:
    lines = [line.strip() for line in prompt_text.splitlines()]
    requests = []
    for line in lines:
        match = re.match(r"^\d+\)\s*(.+)$", line)
        if match:
            requests.append(match.group(1).strip())
    return requests


def _slug(name: str) -> str:
    raw = re.sub(r"[^a-zA-Z0-9]+", "_", name.lower()).strip("_")
    return raw or "generated_case"


def _login_steps(username: str, password: str) -> list[dict]:
    return [
        {"action": "fill", "selector": "#user-name", "value": username, "timeout_ms": 5000},
        {"action": "fill", "selector": "#password", "value": password, "timeout_ms": 5000},
        {"action": "click", "selector": "#login-button", "timeout_ms": 5000},
    ]


def _build_case_from_text(request_text: str) -> dict:
    lowered = request_text.lower()
    username, password = _extract_credentials(request_text)

    if "invalid login" in lowered:
        return {
            "test_name": f"invalid_login_{username}_{password}",
            "description": request_text,
            "path": "/",
            "steps": _login_steps(username, password)
            + [
                {"action": "wait_for_selector", "selector": "[data-test='error']", "timeout_ms": 5000},
                {"action": "expect_text", "selector": "[data-test='error']", "expected": "Epic sadface", "timeout_ms": 5000},
            ],
        }

    if "valid login" in lowered:
        return {
            "test_name": f"valid_login_{username}",
            "description": request_text,
            "path": "/",
            "steps": _login_steps(username, password)
            + [
                {"action": "expect_url_contains", "expected": "/inventory.html", "timeout_ms": 5000},
                {"action": "expect_text", "selector": "[data-test='title']", "expected": "Products", "timeout_ms": 5000},
            ],
        }

    if "add" in lowered and "cart" in lowered and ("checkout" in lowered or "heckout" in lowered):
        product_match = re.search(r'"([^"]+)"', request_text)
        product_name = product_match.group(1) if product_match else "Sauce Labs Fleece Jacket"
        return {
            "test_name": f"login_add_to_cart_checkout_{_slug(product_name)}",
            "description": request_text,
            "path": "/",
            "steps": _login_steps("standard_user", "secret_sauce")
            + [
                {"action": "click", "selector": "[data-test='add-to-cart-sauce-labs-fleece-jacket']", "timeout_ms": 5000},
                {"action": "click", "selector": ".shopping_cart_link", "timeout_ms": 5000},
                {"action": "expect_text", "selector": ".inventory_item_name", "expected": product_name, "timeout_ms": 5000},
                {"action": "click", "selector": "[data-test='checkout']", "timeout_ms": 5000},
                {"action": "fill", "selector": "[data-test='firstName']", "value": "Auto", "timeout_ms": 5000},
                {"action": "fill", "selector": "[data-test='lastName']", "value": "User", "timeout_ms": 5000},
                {"action": "fill", "selector": "[data-test='postalCode']", "value": "12345", "timeout_ms": 5000},
                {"action": "click", "selector": "[data-test='continue']", "timeout_ms": 5000},
                {"action": "click", "selector": "[data-test='finish']", "timeout_ms": 5000},
                {"action": "expect_text", "selector": "[data-test='complete-header']", "expected": "Thank you for your order!", "timeout_ms": 5000},
            ],
        }

    return {
        "test_name": _slug(request_text),
        "description": request_text,
        "path": "/",
        "steps": [{"action": "expect_title_contains", "expected": "Swag Labs", "timeout_ms": 5000}],
    }


def build_plan_offline(prompt_text: str) -> str:
    request_items = _extract_numbered_requests(prompt_text)
    if not request_items:
        request_items = [prompt_text.strip()]

    plan = {
        "app_name": _extract_target_app(prompt_text),
        "test_cases": [_build_case_from_text(item) for item in request_items[:5]],
    }
    return json.dumps(plan)


def load_prompt_text(prompt: Optional[str], prompt_file: Optional[str]) -> str:
    if prompt:
        return prompt

    if prompt_file:
        return Path(prompt_file).read_text().strip()

    raise ValueError("Provide --prompt or --prompt-file")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate UI pytest tests from a natural language prompt")
    parser.add_argument("--prompt", type=str, help="Inline prompt describing UI tests")
    parser.add_argument("--prompt-file", type=str, help="Path to a text file with prompt content")
    parser.add_argument("--plan-file", type=str, help="Optional existing JSON plan file (skip LLM call)")
    parser.add_argument("--offline", action="store_true", help="Generate plan with local prompt parser (no OpenAI call)")
    parser.add_argument("--save-plan", type=str, default="generated/test_plan_from_prompt.json")
    parser.add_argument("--output", type=str, default="tests/test_generated_from_prompt.py")

    args = parser.parse_args()

    if args.plan_file:
        raw_plan = Path(args.plan_file).read_text()
    else:
        prompt_text = load_prompt_text(args.prompt, args.prompt_file)
        if args.offline:
            raw_plan = build_plan_offline(prompt_text)
        else:
            model_output = request_plan_from_model(prompt_text)
            raw_plan = extract_json(model_output)

    plan = UITestPlanModel.model_validate_json(raw_plan)

    save_plan_path = Path(args.save_plan)
    save_plan_path.parent.mkdir(parents=True, exist_ok=True)
    save_plan_path.write_text(json.dumps(plan.model_dump(), indent=2))

    output_path = Path(args.output)
    generate_pytest_from_ui_plan(plan, output_path)

    print(f"Saved validated plan to: {save_plan_path}")
    print(f"Generated pytest file: {output_path}")


if __name__ == "__main__":
    main()
