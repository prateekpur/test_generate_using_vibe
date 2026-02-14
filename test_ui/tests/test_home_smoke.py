from pages.home_page import HomePage


def test_home_page_title_contains_expected_text(page, base_url):
    home_page = HomePage(page, base_url)
    home_page.open()

    assert "Example Domain" in home_page.title()
