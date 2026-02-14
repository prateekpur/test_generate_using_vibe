# test_ui

Minimal UI automation test framework using **pytest + Playwright (Python)**.

## Structure

```text
test_ui/
├── conftest.py
├── generators/
│   └── ui_pytest_generator.py
├── prompts/
│   ├── sample_ui_plan.json
│   └── sample_ui_prompt.txt
├── pytest.ini
├── requirements.txt
├── schemas/
│   └── ui_test_plan_model.py
├── scripts/
│   └── generate_ui_tests_from_prompt.py
├── pages/
│   ├── base_page.py
│   └── home_page.py
└── tests/
    └── test_home_smoke.py
```

## Setup

From inside `test_ui/`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

## Run tests

```bash
pytest
```

Run in headed mode:

```bash
pytest --headed
```

## Base URL configuration

By default tests run against `https://example.com`.

To target your app:

```bash
export UI_BASE_URL="http://127.0.0.1:3000"
pytest
```

## Generate UI tests from prompts

You can generate pytest Playwright tests from a natural-language prompt.

### Option A: Generate from an LLM prompt

```bash
export OPENAI_API_KEY="<your_api_key>"
# optional (defaults shown)
export OPENAI_MODEL="gpt-4o-mini"
# export OPENAI_BASE_URL="https://api.openai.com/v1"

python3 scripts/generate_ui_tests_from_prompt.py \
    --prompt-file prompts/sample_ui_prompt.txt \
    --save-plan generated/test_plan_from_prompt.json \
    --output tests/test_generated_from_prompt.py
```

### Option B: Generate without calling an LLM (from a local plan)

```bash
python3 scripts/generate_ui_tests_from_prompt.py \
    --plan-file prompts/sample_ui_plan.json \
    --save-plan generated/test_plan_from_prompt.json \
    --output tests/test_generated_from_prompt.py
```

Run generated tests:

```bash
pytest -q tests/test_generated_from_prompt.py
```

### Supported step actions in prompt plans

- `goto`
- `click`
- `fill`
- `press`
- `expect_text`
- `expect_title_contains`
- `expect_url_contains`
- `wait_for_selector`

## Notes

- Test design uses a simple Page Object Model (`pages/`).
- Add new page objects under `pages/` and corresponding tests under `tests/`.
