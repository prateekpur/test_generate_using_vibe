class BasePage:
    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self, path: str = "/"):
        normalized_path = path if path.startswith("/") else f"/{path}"
        self.page.goto(f"{self.base_url}{normalized_path}")
