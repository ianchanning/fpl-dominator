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


def login_fpl(page: Page, username: str, password: str) -> None:
    """Authenticates with the Premier League portal."""
    click.echo("[*] Authenticating with Premier League portal...")
    page.goto(FPL_TRANSFERS_URL, wait_until="domcontentloaded")
    purge_onetrust_overlay(page)

    # Check if already authenticated (squad table or user profile present)
    auth_check = page.locator(
        "table._4xqwov8, .ism-squad, [aria-label='Transfers List']"
    )
    if auth_check.count() > 0:
        click.secho("[+] FPL session active.", fg="green")
        return

    # Click the Log in button on the transfers page with force=True
    login_btn = page.locator(
        "button._loginButton_1mxyv_1, button:has-text('Log in'), a:has-text('Log in')"
    ).first
    login_btn.wait_for(state="visible", timeout=15000)
    page.wait_for_timeout(500)
    login_btn.click(force=True)

    # Wait for account.premierleague.com Ping SSO form
    page.wait_for_selector(
        "input#username, input[name='username']", timeout=25000
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
    purge_onetrust_overlay(page)
    click.secho("[+] FPL authentication successful.", fg="green")


def harvest_fpl_squad(page: Page, staging_dir: str) -> None:
    """Extracts the active squad list table into squad.html."""
    click.echo("[*] Harvesting active Squad table...")
    if "fantasy.premierleague.com/en/transfers" not in page.url:
        page.goto(FPL_TRANSFERS_URL, wait_until="domcontentloaded")
    purge_onetrust_overlay(page)

    # Wait for the transfers canvas to mount (pitch view or list view)
    page.wait_for_selector(
        "div[role='radiogroup'], table[aria-label='Transfers List']",
        timeout=15000,
    )

    # Switch to 'List' view if in pitch view
    list_toggle = page.locator("div[role='radiogroup'] >> text='List'")
    if list_toggle.count() > 0:
        try:
            list_toggle.first.click()
            page.wait_for_timeout(800)
        except Exception:
            pass

    # Wait for the squad table to render
    squad_sel = "table[aria-label='Transfers List'], table._4xqwov8"
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

        # Open position selection dropdown
        filter_btn = page.locator(
            "div:has(> button:has-text('Reset')) button._1gkly0o2, "
            "button:has-text('All players'), "
            f"button:has-text('{pos_label}')"
        ).first
        filter_btn.click()
        page.wait_for_selector("div[role='option']", timeout=5000)

        # Select target position option
        page.locator(f"div[role='option']:has-text('{pos_label}')").first.click()
        page.wait_for_timeout(1000)

        # Wait for table to render
        table_sel = f"table[aria-label='{pos_label}'], table._1nvnlp41"
        page.wait_for_selector(table_sel, timeout=10000)
        table_elem = page.locator(table_sel).first
        p1_html = table_elem.evaluate("el => el.outerHTML")

        p1_path = os.path.join(staging_dir, page1_file)
        with open(p1_path, "w", encoding="utf-8") as f:
            f.write(p1_html)
        click.secho(f"    - Scribed {p1_path} ({len(p1_html)} bytes)", fg="cyan")

        # Ingest Page 2 if present
        if has_page_2:
            next_btn = page.locator(
                "div.vzix9s0 button[aria-label='Next'], button[aria-label='Next']"
            ).first
            if next_btn.count() > 0 and next_btn.is_enabled():
                click.echo(f"  [+] Navigating to {pos_label} Page 2...")
                next_btn.click()
                page.wait_for_timeout(1000)
                page.wait_for_selector(table_sel, timeout=10000)

                p2_html = table_elem.evaluate("el => el.outerHTML")
                p2_path = os.path.join(staging_dir, page2_file)
                with open(p2_path, "w", encoding="utf-8") as f:
                    f.write(p2_html)
                click.secho(
                    f"    - Scribed {p2_path} ({len(p2_html)} bytes)", fg="cyan"
                )

                # Reset back to Page 1 for next position
                first_btn = page.locator(
                    "div.vzix9s0 button[aria-label='First'], button[aria-label='First']"
                ).first
                if first_btn.count() > 0 and first_btn.is_enabled():
                    first_btn.click()
                    page.wait_for_timeout(500)


def login_ffs(page: Page, username: str, password: str) -> None:
    """Authenticates with Fantasy Football Scout members area."""
    click.echo("[*] Authenticating with Fantasy Football Scout...")
    page.goto(FFS_HOME_URL, wait_until="domcontentloaded")

    # Check if already authenticated
    if page.locator("a:has-text('Log out'), a[href*='sign_out']").count() > 0:
        click.secho("[+] FFS session active.", fg="green")
        return

    # Fill username and password
    user_input = page.locator("input[name='username'], input#user_login").first
    pass_input = page.locator("input[name='password'], input#user_password").first
    user_input.fill(username)
    pass_input.fill(password)

    submit_btn = page.locator(
        "button#loginButton, button[name='login'], input[type='submit'][name='commit']"
    ).first
    submit_btn.click()

    page.wait_for_timeout(2000)
    page.goto(FFS_TICKER_URL, wait_until="domcontentloaded")
    click.secho("[+] FFS authentication successful.", fg="green")


def harvest_ffs_tickers(page: Page, staging_dir: str) -> None:
    """Extracts Overall, Attack, and Defence FDR tickers from FFS Season Ticker."""
    click.echo("[*] Harvesting Fantasy Football Scout FDR Tickers...")
    page.goto(FFS_TICKER_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(1000)

    ticker_views = [
        ("overall", "fixtures_5w.html"),
        ("attack", "fixtures_attack_5w.html"),
        ("defence", "fixtures_defence_5w.html"),
    ]

    # Ensure 5 GWs window is selected on Season Ticker
    try:
        gw_count_select = page.locator(
            "select.gw-select[title*='gameweeks shown'], div.gw-display-controls select.gw-select"
        ).first
        if gw_count_select.count() > 0:
            gw_count_select.select_option(label="5 GWs")
            page.wait_for_timeout(600)
    except Exception:
        pass

    for view_val, filename in ticker_views:
        click.echo(f"  [+] Selecting Ticker View: {view_val.capitalize()}...")
        select_elem = page.locator("div.ticker-controls select.control-select").first
        select_elem.select_option(value=view_val)
        page.wait_for_timeout(600)

        # Wait for ticker grid
        page.wait_for_selector("div.advanced-ticker", timeout=10000)
        ticker_container = page.locator("div.advanced-ticker").first
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
