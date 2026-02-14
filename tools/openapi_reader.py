from pathlib import Path
import json
import yaml
import requests


def read_openapi(source: str):
    """
    source can be:
      - local file path (openapi.yaml / openapi.json)
      - http(s) URL
    """

    if source.startswith("http://") or source.startswith("https://"):
        resp = requests.get(source, timeout=10)
        resp.raise_for_status()

        text = resp.text
    else:
        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(f"OpenAPI file not found: {source}")

        text = path.read_text(encoding="utf-8")

    # try JSON first, then YAML
    try:
        spec = json.loads(text)
    except json.JSONDecodeError:
        spec = yaml.safe_load(text)

    return spec
