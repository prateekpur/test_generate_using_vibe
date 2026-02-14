import os
import pytest
from playwright.sync_api import sync_playwright


def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed mode",
    )
    parser.addoption(
        "--slowmo",
        action="store",
        type=int,
        default=0,
        help="Delay Playwright actions by N milliseconds",
    )


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("UI_BASE_URL", "https://example.com")


@pytest.fixture(scope="session")
def browser(pytestconfig):
    headed = pytestconfig.getoption("headed")
    slowmo = pytestconfig.getoption("slowmo")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not headed, slow_mo=slowmo)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()

    yield page

    context.close()
