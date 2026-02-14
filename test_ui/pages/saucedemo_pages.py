from .base_page import BasePage
from .timeouts import DEFAULT_TIMEOUT_MS


class SauceLoginPage(BasePage):
    def open(self):
        super().open("/")

    def login(self, username: str, password: str, timeout_ms: int = DEFAULT_TIMEOUT_MS):
        self.page.locator("#user-name").fill(username, timeout=timeout_ms)
        self.page.locator("#password").fill(password, timeout=timeout_ms)
        self.page.locator("#login-button").click(timeout=timeout_ms)

    def expect_error_contains(self, text: str = "Epic sadface", timeout_ms: int = DEFAULT_TIMEOUT_MS):
        self.page.wait_for_selector("[data-test='error']", timeout=timeout_ms)
        assert text in self.page.locator("[data-test='error']").inner_text(timeout=timeout_ms)


class SauceInventoryPage(BasePage):
    def expect_url_contains(self, value: str):
        assert value in self.page.url

    def expect_title_contains(self, text: str, timeout_ms: int = DEFAULT_TIMEOUT_MS):
        assert text in self.page.locator("[data-test='title']").inner_text(timeout=timeout_ms)

    def add_fleece_jacket_to_cart(self, timeout_ms: int = DEFAULT_TIMEOUT_MS):
        self.page.locator("[data-test='add-to-cart-sauce-labs-fleece-jacket']").click(timeout=timeout_ms)

    def open_cart(self, timeout_ms: int = DEFAULT_TIMEOUT_MS):
        self.page.locator(".shopping_cart_link").click(timeout=timeout_ms)


class SauceCartPage(BasePage):
    def expect_item_in_cart(self, item_name: str, timeout_ms: int = DEFAULT_TIMEOUT_MS):
        assert item_name in self.page.locator(".inventory_item_name").inner_text(timeout=timeout_ms)

    def start_checkout(self, timeout_ms: int = DEFAULT_TIMEOUT_MS):
        self.page.locator("[data-test='checkout']").click(timeout=timeout_ms)


class SauceCheckoutPage(BasePage):
    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str, timeout_ms: int = DEFAULT_TIMEOUT_MS):
        self.page.locator("[data-test='firstName']").fill(first_name, timeout=timeout_ms)
        self.page.locator("[data-test='lastName']").fill(last_name, timeout=timeout_ms)
        self.page.locator("[data-test='postalCode']").fill(postal_code, timeout=timeout_ms)
        self.page.locator("[data-test='continue']").click(timeout=timeout_ms)

    def finish(self, timeout_ms: int = DEFAULT_TIMEOUT_MS):
        self.page.locator("[data-test='finish']").click(timeout=timeout_ms)

    def expect_completion_message(self, text: str = "Thank you for your order!", timeout_ms: int = DEFAULT_TIMEOUT_MS):
        assert text in self.page.locator("[data-test='complete-header']").inner_text(timeout=timeout_ms)
