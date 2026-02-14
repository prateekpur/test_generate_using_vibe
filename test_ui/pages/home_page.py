from .base_page import BasePage


class HomePage(BasePage):
    def open(self):
        super().open("/")

    def title(self) -> str:
        return self.page.title()
