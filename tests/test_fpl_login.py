"""Targeted Authentication Test Battery for FPL & Fantasy Football Scout (RFC-012).

Tests only the live authentication flows against Premier League Ping SSO
and Fantasy Football Scout Members Portal, validating that session tokens
are acquired, overlays are neutralized, and authenticated views render.

Can be run via:
    uv run python tests/test_fpl_login.py [--headed]
or:
    uv run python -m unittest -v tests.test_fpl_login
"""

import os
import sys
import unittest
from typing import Optional

from dotenv import load_dotenv
from playwright.sync_api import Page, sync_playwright

load_dotenv()

FPL_TRANSFERS_URL = "https://fantasy.premierleague.com/en/transfers"
FFS_HOME_URL = "https://members.fantasyfootballscout.co.uk/"
FFS_TICKER_URL = "https://members.fantasyfootballscout.co.uk/season-ticker/"

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def purge_onetrust_overlay(page: Page) -> None:
    """Neutralizes OneTrust banner and pointer-intercepting dark filters."""
    try:
        page.wait_for_selector(
            "#onetrust-accept-btn-handler, button:has-text('Accept All Cookies')",
            timeout=3500,
        )
    except Exception:
        pass

    try:
        accept_btn = page.locator(
            "#onetrust-accept-btn-handler, button:has-text('Accept All Cookies')"
        )
        if accept_btn.count() > 0 and accept_btn.first.is_visible():
            accept_btn.first.click()
            page.wait_for_timeout(400)
    except Exception:
        pass

    # Aggressive DOM neutralization to ensure pointer events are never blocked
    try:
        page.evaluate(
            """() => {
            const sdk = document.getElementById('onetrust-consent-sdk');
            if (sdk) sdk.remove();
            const filters = document.querySelectorAll('.onetrust-pc-dark-filter, #onetrust-banner-sdk');
            filters.forEach(f => f.remove());
        }"""
        )
    except Exception:
        pass


def execute_fpl_login_flow(
    page: Page,
    username: str,
    password: str,
    screenshot_path: Optional[str] = None,
) -> bool:
    """Executes and verifies FPL Ping SSO authentication."""
    page.goto(FPL_TRANSFERS_URL, wait_until="domcontentloaded")
    purge_onetrust_overlay(page)

    # Check if session is already active
    auth_check = page.locator(
        "table._4xqwov8, .ism-squad, [aria-label='Transfers List']"
    )
    if auth_check.count() > 0:
        return True

    # Click Log in button with force=True to bypass lingering overlays
    login_btn = page.locator(
        "button._loginButton_1mxyv_1, button:has-text('Log in'), a:has-text('Log in')"
    ).first
    login_btn.wait_for(state="visible", timeout=15000)
    page.wait_for_timeout(500)
    login_btn.click(force=True)

    # Wait for Ping SSO form
    page.wait_for_selector(
        "input#username, input[name='username']", timeout=20000
    )
    purge_onetrust_overlay(page)

    # Fill credentials
    page.locator("input#username, input[name='username']").first.fill(username)
    page.locator("input#password, input[name='password']").first.fill(password)

    # Submit login
    sign_in_btn = page.locator(
        "button#btnSignIn, button[data-skbuttonvalue='SIGNON'], "
        "form#usernamePasswordForm button[type='submit']"
    ).first
    sign_in_btn.click()

    # Wait for redirection out of account.premierleague.com back to fantasy
    page.wait_for_url(
        lambda u: "account.premierleague.com" not in u
        and "fantasy.premierleague.com" in u,
        timeout=25000,
    )
    page.wait_for_timeout(2000)

    # Navigate to Transfers view and verify tables render
    page.goto(FPL_TRANSFERS_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    if screenshot_path:
        page.screenshot(path=screenshot_path)

    # Verify at least one player or squad table is present
    tables_count = page.locator("table._1nvnlp41, table._4xqwov8").count()
    return tables_count > 0


def execute_ffs_login_flow(
    page: Page,
    username: str,
    password: str,
    screenshot_path: Optional[str] = None,
) -> bool:
    """Executes and verifies Fantasy Football Scout authentication."""
    page.goto(FFS_HOME_URL, wait_until="domcontentloaded")

    # Check if already authenticated
    if page.locator("a:has-text('Log out'), a[href*='sign_out']").count() > 0:
        return True

    # Fill credentials on members homepage
    user_input = page.locator("input[name='username'], input#user_login").first
    pass_input = page.locator("input[name='password'], input#user_password").first
    user_input.fill(username)
    pass_input.fill(password)

    # Submit
    submit_btn = page.locator(
        "button#loginButton, button[name='login'], input[type='submit'][name='commit']"
    ).first
    submit_btn.click()
    page.wait_for_timeout(2000)

    # Navigate to Season Ticker
    page.goto(FFS_TICKER_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    if screenshot_path:
        page.screenshot(path=screenshot_path)

    ticker_count = page.locator(
        "div#fpl-ticker-root, div.advanced-ticker"
    ).count()
    return ticker_count > 0


class TestLiveAuthentication(unittest.TestCase):
    """Live authentication validation tests."""

    def setUp(self):
        if os.environ.get("RUN_LIVE_TESTS") != "1":
            self.skipTest(
                "Skipping live auth test during general discovery. "
                "Run explicitly via `uv run python tests/test_fpl_login.py` "
                "or set RUN_LIVE_TESTS=1."
            )
        self.fpl_user = os.environ.get("FPL_LOGIN")
        self.fpl_pass = os.environ.get("FPL_PASS")
        self.ffs_user = os.environ.get("FFS_LOGIN")
        self.ffs_pass = os.environ.get("FFS_PASS")

    def test_fpl_live_login_flow(self):
        """Verifies that FPL Ping SSO authenticates and loads transfers."""
        if not self.fpl_user or not self.fpl_pass:
            self.skipTest("FPL credentials missing in environment / .env")

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox"],
            )
            page = browser.new_page(
                viewport={"width": 1920, "height": 1080},
                user_agent=USER_AGENT,
            )
            try:
                success = execute_fpl_login_flow(
                    page, self.fpl_user, self.fpl_pass
                )
                self.assertTrue(
                    success,
                    "FPL login succeeded but transfers tables failed to render.",
                )
            finally:
                browser.close()

    def test_ffs_live_login_flow(self):
        """Verifies that FFS members authentication loads season ticker."""
        if not self.ffs_user or not self.ffs_pass:
            self.skipTest("FFS credentials missing in environment / .env")

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox"],
            )
            page = browser.new_page(
                viewport={"width": 1920, "height": 1080},
                user_agent=USER_AGENT,
            )
            try:
                success = execute_ffs_login_flow(
                    page, self.ffs_user, self.ffs_pass
                )
                self.assertTrue(
                    success,
                    "FFS login succeeded but season ticker failed to render.",
                )
            finally:
                browser.close()


if __name__ == "__main__":
    is_headed = "--headed" in sys.argv
    print(f"=== TESTING LIVE AUTHENTICATION (Headed={is_headed}) ===")

    fpl_u = os.environ.get("FPL_LOGIN")
    fpl_p = os.environ.get("FPL_PASS")
    ffs_u = os.environ.get("FFS_LOGIN")
    ffs_p = os.environ.get("FFS_PASS")

    if not fpl_u or not fpl_p:
        print("ERROR: FPL_LOGIN / FPL_PASS missing in .env")
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=not is_headed,
            slow_mo=500 if is_headed else 0,
            args=["--no-sandbox", "--disable-setuid-sandbox"],
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent=USER_AGENT,
        )
        page = context.new_page()

        print("[*] Testing FPL Login Flow...")
        fpl_ok = execute_fpl_login_flow(
            page, fpl_u, fpl_p, screenshot_path="fpl_login_success.png"
        )
        if fpl_ok:
            print(">>> FPL AUTHENTICATION SUCCESSFUL! Transfers view verified.")
        else:
            print(">>> FPL AUTHENTICATION FAILED!")

        if ffs_u and ffs_p:
            print("[*] Testing FFS Login Flow...")
            ffs_ok = execute_ffs_login_flow(
                page, ffs_u, ffs_p, screenshot_path="ffs_login_success.png"
            )
            if ffs_ok:
                print(">>> FFS AUTHENTICATION SUCCESSFUL! Season ticker verified.")
            else:
                print(">>> FFS AUTHENTICATION FAILED!")

        browser.close()
    print("=== LIVE AUTH TEST COMPLETE ===")
