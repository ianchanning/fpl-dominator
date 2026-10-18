"""Automated Headless Ingestion Pipeline via Playwright (RFC-012).

Navigates FPL Transfers and Fantasy Football Scout Season Ticker portals,
extracts all 12 raw outer HTML artifacts into atomic staging, verifies them
against the RFC-012 Vault Contract, and promotes them to the active vault.
"""

import os
import shutil
import sys
from typing import Optional

import click
from dotenv import load_dotenv
from playwright.sync_api import BrowserContext, Page, sync_playwright

from fpl_dominator.vault_contract import (
    VaultContractViolationError,
    verify_vault_contract,
)

FPL_TRANSFERS_URL = "https://fantasy.premierleague.com/transfers"
FPL_LOGIN_URL = "https://users.premierleague.com/"
FFS_TICKER_URL = "https://members.fantasyfootballscout.co.uk/season-ticker/"
FFS_LOGIN_URL = "https://members.fantasyfootballscout.co.uk/users/sign_in"

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def dismiss_onetrust_cookie_banner(page: Page) -> None:
    """Dismisses OneTrust cookie consent banner if present."""
    try:
        banner_btn = page.locator("#onetrust-accept-btn-handler")
        if banner_btn.is_visible(timeout=3000):
            banner_btn.click()
            page.wait_for_timeout(500)
    except Exception:
        pass


def login_fpl(page: Page, username: str, password: str) -> None:
    """Authenticates with the Premier League portal."""
    click.echo("[*] Authenticating with Premier League portal...")
    page.goto(FPL_TRANSFERS_URL, wait_until="domcontentloaded")
    dismiss_onetrust_cookie_banner(page)

    # Check if already authenticated (squad table or user profile present)
    auth_check = page.locator(
        "table._4xqwov8, .ism-squad, [aria-label='Transfers List']"
    )
    if auth_check.count() > 0:
        click.secho("[+] FPL session active.", fg="green")
        return

    # Check for login button or redirect to login endpoint
    login_btn = page.locator(
        "a:has-text('Sign In'), button:has-text('Sign In'), "
        "a[href*='users.premierleague.com']"
    )
    if login_btn.count() > 0 and login_btn.first.is_visible():
        login_btn.first.click()
        page.wait_for_load_state("domcontentloaded")
    else:
        page.goto(FPL_LOGIN_URL, wait_until="domcontentloaded")

    dismiss_onetrust_cookie_banner(page)

    # Fill credentials
    page.locator("input#login-username, input[name='login']").first.fill(username)
    page.locator("input#login-password, input[name='password']").first.fill(password)
    page.locator("button[type='submit']").first.click()

    # Wait for post-login redirection back to transfers
    page.wait_for_url(lambda u: "fantasy.premierleague.com" in u, timeout=15000)
    page.goto(FPL_TRANSFERS_URL, wait_until="networkidle")
    dismiss_onetrust_cookie_banner(page)
    click.secho("[+] FPL authentication successful.", fg="green")


def harvest_fpl_squad(page: Page, staging_dir: str) -> None:
    """Extracts the active squad list table into squad.html."""
    click.echo("[*] Harvesting active Squad table...")
    page.goto(FPL_TRANSFERS_URL, wait_until="networkidle")
    dismiss_onetrust_cookie_banner(page)

    # Switch to 'List' view if in pitch view
    list_toggle = page.locator(
        "button.ktbkv41.ktbkv40._4xqwov0, button:has-text('List'), "
        "[aria-label='List view']"
    )
    if list_toggle.count() > 0 and list_toggle.first.is_visible():
        try:
            list_toggle.first.click()
            page.wait_for_timeout(500)
        except Exception:
            pass

    # Wait for the squad table to render
    squad_sel = "table._4xqwov8, table[aria-label='Transfers List']"
    page.wait_for_selector(squad_sel, timeout=10000)
    squad_table = page.locator(squad_sel).first
    squad_html = squad_table.evaluate("el => el.outerHTML")

    out_path = os.path.join(staging_dir, "squad.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(squad_html)
    click.secho(f"    - Scribed {out_path} ({len(squad_html)} bytes)", fg="cyan")


def harvest_fpl_positions(page: Page, staging_dir: str) -> None:
    """Extracts all position tables across Page 1 and Page 2."""
    click.echo("[*] Harvesting Player Market position tables...")

    positions = [
        ("Goalkeepers", "goalkeepers.html", "goalkeepers_2.html", True),
        ("Defenders", "defenders.html", "defenders_2.html", True),
        ("Midfielders", "midfielders.html", "midfielders_2.html", True),
        ("Forwards", "forwards.html", "forwards_2.html", True),
    ]

    for pos_label, page1_file, page2_file, has_page_2 in positions:
        click.echo(f"  [+] Selecting position: {pos_label}...")

        # Open React-Aria dropdown
        dropdown_btn = page.locator(
            "div.react-aria-Select button, button[aria-haspopup='listbox'], "
            "button[id^='react-aria']"
        ).first
        dropdown_btn.click()
        page.wait_for_selector("[role='listbox'], [role='option']", timeout=5000)

        # Select target position option
        page.locator(f"[role='option']:has-text('{pos_label}')").first.click()
        page.wait_for_timeout(600)

        # Wait for table rows to stabilize
        page.wait_for_selector("table._1nvnlp41, tr._1trl5ao0", timeout=10000)
        table_elem = page.locator("table._1nvnlp41, div._1nvnlp49 table").first
        p1_html = table_elem.evaluate("el => el.outerHTML")

        p1_path = os.path.join(staging_dir, page1_file)
        with open(p1_path, "w", encoding="utf-8") as f:
            f.write(p1_html)
        click.secho(f"    - Scribed {p1_path} ({len(p1_html)} bytes)", fg="cyan")

        # Ingest Page 2 if present
        if has_page_2:
            page2_btn = page.locator(
                "nav[aria-label='Pagination'] button:has-text('2'), "
                "button[aria-label='Next page'], "
                "div._1nvnlp40 nav button:nth-child(2)"
            )
            if page2_btn.count() > 0 and page2_btn.first.is_visible():
                click.echo(f"  [+] Navigating to {pos_label} Page 2...")
                page2_btn.first.click()
                page.wait_for_timeout(800)
                page.wait_for_selector("table._1nvnlp41, tr._1trl5ao0", timeout=10000)

                p2_html = table_elem.evaluate("el => el.outerHTML")
                p2_path = os.path.join(staging_dir, page2_file)
                with open(p2_path, "w", encoding="utf-8") as f:
                    f.write(p2_html)
                click.secho(
                    f"    - Scribed {p2_path} ({len(p2_html)} bytes)", fg="cyan"
                )

                # Reset back to Page 1 for next position
                page1_btn = page.locator(
                    "nav[aria-label='Pagination'] button:has-text('1')"
                )
                if page1_btn.count() > 0 and page1_btn.first.is_visible():
                    page1_btn.first.click()
                    page.wait_for_timeout(400)


def login_ffs(page: Page, username: str, password: str) -> None:
    """Authenticates with Fantasy Football Scout members area."""
    click.echo("[*] Authenticating with Fantasy Football Scout...")
    page.goto(FFS_LOGIN_URL, wait_until="domcontentloaded")

    # Check if already authenticated
    if page.locator("a:has-text('Log out'), a[href*='sign_out']").count() > 0:
        click.secho("[+] FFS session active.", fg="green")
        return

    page.locator("input#user_login").fill(username)
    page.locator("input#user_password").fill(password)
    page.locator("input[type='submit'][name='commit']").click()

    page.wait_for_url(lambda u: "users/sign_in" not in u, timeout=15000)
    click.secho("[+] FFS authentication successful.", fg="green")


def harvest_ffs_tickers(page: Page, staging_dir: str) -> None:
    """Extracts Overall, Attack, and Defence FDR tickers from FFS Season Ticker."""
    click.echo("[*] Harvesting Fantasy Football Scout FDR Tickers...")
    page.goto(FFS_TICKER_URL, wait_until="networkidle")

    ticker_views = [
        ("All", "fixtures_5w.html"),
        ("Attack", "fixtures_attack_5w.html"),
        ("Defence", "fixtures_defence_5w.html"),
    ]

    for view_label, filename in ticker_views:
        click.echo(f"  [+] Selecting Ticker View: {view_label}...")
        select_elem = page.locator("div.ticker-controls select.control-select").first

        # Select view
        try:
            select_elem.select_option(label=view_label)
        except Exception:
            select_elem.select_option(value=view_label.lower())
        page.wait_for_timeout(600)

        # Wait for ticker grid
        page.wait_for_selector(
            "div#fpl-ticker-root div.advanced-ticker, .team-row", timeout=10000
        )
        ticker_container = page.locator("div#fpl-ticker-root div.advanced-ticker").first
        ticker_html = ticker_container.evaluate("el => el.outerHTML")

        out_path = os.path.join(staging_dir, filename)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(ticker_html)
        click.secho(f"    - Scribed {out_path} ({len(ticker_html)} bytes)", fg="cyan")


def execute_headless_ingestion(
    gameweek_dir: str,
    headless: bool = True,
    storage_state_path: Optional[str] = None,
) -> None:
    """Executes the full automated ingestion ritual and verifies vault contract."""
    load_dotenv()

    fpl_user = os.environ.get("FPL_LOGIN")
    fpl_pass = os.environ.get("FPL_PASS")
    ffs_user = os.environ.get("FFS_LOGIN")
    ffs_pass = os.environ.get("FFS_PASS")

    if not all([fpl_user, fpl_pass, ffs_user, ffs_pass]):
        missing = [
            k
            for k, v in [
                ("FPL_LOGIN", fpl_user),
                ("FPL_PASS", fpl_pass),
                ("FFS_LOGIN", ffs_user),
                ("FFS_PASS", ffs_pass),
            ]
            if not v
        ]
        click.secho(
            f"Error: Missing required credentials in environment: {missing}\n"
            f"Set them in .env or provide via GitHub Secrets.",
            fg="red",
            err=True,
        )
        sys.exit(1)

    staging_dir = os.path.join(gameweek_dir, ".staging")
    os.makedirs(staging_dir, exist_ok=True)

    click.secho(
        f"=== INITIATING AUTOMATED INGESTION FOR {gameweek_dir.upper()} ===",
        fg="magenta",
        bold=True,
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=["--no-sandbox", "--disable-setuid-sandbox"],
        )

        context_kwargs = {
            "viewport": {"width": 1920, "height": 1080},
            "user_agent": USER_AGENT,
        }
        if storage_state_path and os.path.exists(storage_state_path):
            context_kwargs["storage_state"] = storage_state_path

        context: BrowserContext = browser.new_context(**context_kwargs)
        page: Page = context.new_page()

        try:
            # 1. Harvest FPL
            login_fpl(page, fpl_user, fpl_pass)
            harvest_fpl_squad(page, staging_dir)
            harvest_fpl_positions(page, staging_dir)

            # 2. Harvest FFS
            login_ffs(page, ffs_user, ffs_pass)
            harvest_ffs_tickers(page, staging_dir)

            # Persist session state if path specified
            if storage_state_path:
                os.makedirs(os.path.dirname(storage_state_path), exist_ok=True)
                context.storage_state(path=storage_state_path)

        finally:
            browser.close()

    # 3. Contract Invariant Gate
    click.echo("\n[*] Summoning Ingestion Contract Oracle to inspect staging...")
    is_valid, violations = verify_vault_contract(staging_dir)

    if not is_valid:
        shutil.rmtree(staging_dir, ignore_errors=True)
        raise VaultContractViolationError(staging_dir, violations)

    click.secho(
        "[+] 100% Invariant Verification Passed. Promoting staging to vault...",
        fg="green",
        bold=True,
    )

    # 4. Atomic Promotion
    for fname in os.listdir(staging_dir):
        src_file = os.path.join(staging_dir, fname)
        dst_file = os.path.join(gameweek_dir, fname)
        shutil.move(src_file, dst_file)

    shutil.rmtree(staging_dir, ignore_errors=True)
    click.secho(
        f"=== SUCCESS: {gameweek_dir.upper()} VAULT FULLY HARVESTED ===",
        fg="green",
        bold=True,
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m fpl_dominator.ingest_playwright gw8")
        sys.exit(1)
    execute_headless_ingestion(sys.argv[1])
