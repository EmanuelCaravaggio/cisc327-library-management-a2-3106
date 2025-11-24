from flask import url_for
from playwright.sync_api import Page, expect
import pytest
import time

URL = "http://localhost:5000"

pytest.skip("Skipping Playwright E2E tests in CI", allow_module_level=True)

@pytest.fixture(scope="session")
def new_isbn():
 return str(int(time.time()))[:13].ljust(13,"0")

def test_add_new_book_and_verify_book_in_catalog(page: Page, new_isbn):

    #adding book
    page.goto(f"{URL}/add_book")

    page.get_by_label("Title").fill("The Great Gatsby")
    page.get_by_label("Author").fill("F. Scott Fitzgerald")
    page.get_by_label("ISBN").fill(new_isbn)
    page.get_by_label("Total Copies").fill("4")

    page.get_by_role("button", name="Add Book to Catalog").click()

    #verifying book was added in catalog
    expect(page.get_by_text("successfully added")).to_be_visible()

def test_navigating_to_borrow_page(page: Page):

    #navigation to page
    page.goto(f"{URL}/catalog")

    row = page.locator("tr", has_text="3214358905437")

    expect(row).to_be_visible()

    expect(row.locator("input[name='patron_id']")).to_be_visible()
    expect(row.get_by_role("button", name="Borrow")).to_be_visible()

def test_borrow_book_and_verify_borrow_confirmaton_message(page: Page):

    #navigaton to page
    page.goto(f"{URL}/catalog")

    row = page.locator("tr", has_text="1234567890123")

    expect(row).to_be_visible()

    row.locator("input[name='patron_id']").fill("654321")

    row.get_by_role("button", name="Borrow").click()

    expect(page.get_by_text("Successfully borrowed")).to_be_visible()
