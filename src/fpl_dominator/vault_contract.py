"""Vault Integrity Contract Verifier (RFC-012 Invariant Gate).

Enforces strict physical and schema laws on Gameweek vault directories
before promoting harvested artifacts or unleashing the solver.
"""

import os
from typing import List, Tuple

from bs4 import BeautifulSoup

REQUIRED_CORE_FILES = [
    "fixtures_5w.html",
    "fixtures_attack_5w.html",
    "fixtures_defence_5w.html",
    "goalkeepers.html",
    "defenders.html",
    "defenders_2.html",
    "midfielders.html",
    "midfielders_2.html",
    "forwards.html",
    "forwards_2.html",
    "squad.html",
]

MIN_FILE_SIZE_BYTES = 1024


class VaultContractViolationError(Exception):
    """Raised when a gameweek vault fails the integrity contract."""

    def __init__(self, vault_dir: str, violations: List[str]):
        self.vault_dir = vault_dir
        self.violations = violations
        msg = (
            f"Vault '{vault_dir}' failed RFC-012 integrity contract with "
            f"{len(violations)} violation(s):\n"
            + "\n".join(f"  - {v}" for v in violations)
        )
        super().__init__(msg)


def verify_vault_contract(
    vault_dir: str, allow_optional_gkp2: bool = True
) -> Tuple[bool, List[str]]:
    """Evaluates the RFC-012 contract against a target vault directory.

    Returns:
        (is_valid, list_of_violations)
    """
    violations: List[str] = []

    if not os.path.isdir(vault_dir):
        return False, [f"Vault directory '{vault_dir}' does not exist."]

    # 1. File Completeness & Non-Trivial Size Checks
    for filename in REQUIRED_CORE_FILES:
        filepath = os.path.join(vault_dir, filename)
        if not os.path.exists(filepath):
            violations.append(f"Missing required artifact: {filename}")
            continue

        size = os.path.getsize(filepath)
        if size < MIN_FILE_SIZE_BYTES:
            violations.append(
                f"File '{filename}' size ({size} bytes) below minimum threshold "
                f"({MIN_FILE_SIZE_BYTES} bytes). Likely empty or stub dump."
            )

    missing_critical = [
        v
        for v in violations
        if "Missing required artifact" in v or "below minimum threshold" in v
    ]
    if len(missing_critical) > 3:
        return False, violations

    # 2. Positional Player HTML Integrity Checks
    pos_specs = [
        ("goalkeepers.html", "GKP", 20),
        ("defenders.html", "DEF", 25),
        ("defenders_2.html", "DEF", 20),
        ("midfielders.html", "MID", 25),
        ("midfielders_2.html", "MID", 20),
        ("forwards.html", "FWD", 25),
        ("forwards_2.html", "FWD", 20),
    ]

    for filename, _pos_label, min_rows in pos_specs:
        filepath = os.path.join(vault_dir, filename)
        if (
            not os.path.exists(filepath)
            or os.path.getsize(filepath) < MIN_FILE_SIZE_BYTES
        ):
            continue

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "lxml")

            rows = soup.select("tr._1trl5ao0")
            if len(rows) < min_rows:
                violations.append(
                    f"{filename}: Found only {len(rows)} player rows "
                    f"(expected >= {min_rows}). Possible React hydration truncation."
                )

            valid_prices = 0
            for row in rows[:10]:
                td_texts = [td.text for td in row.select("td")]
                if any("£" in t for t in td_texts):
                    valid_prices += 1

            if rows and valid_prices == 0:
                violations.append(
                    f"{filename}: Extracted rows lack valid '£' price cells."
                )
        except Exception as e:
            violations.append(f"{filename}: Failed to parse HTML: {e}")

    # 3. Squad HTML Integrity Check
    squad_path = os.path.join(vault_dir, "squad.html")
    has_squad = (
        os.path.exists(squad_path)
        and os.path.getsize(squad_path) >= MIN_FILE_SIZE_BYTES
    )
    if has_squad:
        try:
            with open(squad_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "lxml")

            squad_rows = soup.select("tr.rweppyb, tr.rweppyc, tr._1trl5ao0")
            if len(squad_rows) != 15:
                violations.append(
                    f"squad.html: Found {len(squad_rows)} squad rows "
                    f"(strictly expected exactly 15)."
                )

            valid_player_names = 0
            for row in squad_rows:
                name_elem = row.select_one("span.rfkqam4")
                if name_elem and name_elem.text.strip():
                    valid_player_names += 1

            if valid_player_names < 15:
                violations.append(
                    f"squad.html: Only {valid_player_names}/15 rows have names."
                )

            price_tds_count = sum(
                1
                for row in squad_rows
                if any("£" in td.text for td in row.select("td"))
            )
            if price_tds_count == 0:
                market_files = [
                    "goalkeepers.html",
                    "defenders.html",
                    "midfielders.html",
                    "forwards.html",
                ]
                missing_market = [
                    f
                    for f in market_files
                    if not os.path.exists(os.path.join(vault_dir, f))
                ]
                if missing_market:
                    violations.append(
                        f"squad.html lacks prices and market fallback files "
                        f"are missing: {missing_market}"
                    )
        except Exception as e:
            violations.append(f"squad.html: Failed to parse squad HTML: {e}")

    # 4. Fixtures HTML Integrity Checks
    fixture_files = [
        "fixtures_5w.html",
        "fixtures_attack_5w.html",
        "fixtures_defence_5w.html",
    ]
    for filename in fixture_files:
        filepath = os.path.join(vault_dir, filename)
        if (
            not os.path.exists(filepath)
            or os.path.getsize(filepath) < MIN_FILE_SIZE_BYTES
        ):
            continue

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "lxml")

            team_rows = soup.select(".team-row")
            if len(team_rows) < 20:
                violations.append(
                    f"{filename}: Found {len(team_rows)} team rows "
                    f"(expected 20 Premier League clubs)."
                )

            gw_headers = [
                h.text.strip() for h in soup.select(".gw-header-btn") if h.text.strip()
            ]
            if len(gw_headers) < 5:
                violations.append(
                    f"{filename}: Found {len(gw_headers)} GW headers "
                    f"(expected >= 5 horizon weeks)."
                )
        except Exception as e:
            violations.append(f"{filename}: Failed to parse ticker HTML: {e}")

    return len(violations) == 0, violations


def assert_vault_contract(vault_dir: str, allow_optional_gkp2: bool = True) -> None:
    """Asserts that the vault satisfies the RFC-012 contract, raising on failure."""
    is_valid, violations = verify_vault_contract(
        vault_dir, allow_optional_gkp2=allow_optional_gkp2
    )
    if not is_valid:
        raise VaultContractViolationError(vault_dir, violations)
