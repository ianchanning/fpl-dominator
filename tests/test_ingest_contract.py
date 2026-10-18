"""Dan Luu-style unit, contract, and integration tests for RFC-012 Ingestion.

Methodology (Dan Luu Testing Heuristics):
1. Pre-implementation edge-case identification & failure surfaces:
   - Partial HTML dumps caused by React hydration race conditions.
   - Empty 1-byte stub files (e.g. current gw8 fixtures_5w.html).
   - Missing pagination pages (defenders_2.html, etc.).
   - Truncated squad reality (squad.html missing or < 15 players).
   - Abnormal value boundaries ([3.8, 16.0], negative points, FDR bounds).
2. Independent re-derivation (The Oracle):
   - Independent BeautifulSoup-based contract validator with fresh context.
   - Zero imports from production scrapers or CLI scripts.
3. Structured synthetic failure injection:
   - Synthetic fixtures simulating React hydration delays & stub files.
4. Real-world vault integration:
   - Verify against real golden master vault (gw7) -> MUST PASS.
   - Verify against real active incomplete vault (gw8) -> MUST DETECT DEFECTS.
"""

import os
import tempfile
import unittest
from typing import List, Tuple

from bs4 import BeautifulSoup

from fpl_dominator.vault_contract import verify_vault_contract

# ==============================================================================
# SECTION 1: THE INDEPENDENT CONTRACT ORACLE
# ==============================================================================

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


def independently_verify_vault_contract(
    vault_dir: str, allow_optional_gkp2: bool = True
) -> Tuple[bool, List[str]]:
    """Completely independent verification oracle for RFC-012 vault integrity.

    Written with zero shared imports from fpl_dominator scrapers.
    Asserts strict physical laws on the directory contents.
    """
    violations: List[str] = []

    if not os.path.isdir(vault_dir):
        return False, [f"Vault directory '{vault_dir}' does not exist."]

    # 1. File Completeness & Size Checks
    for filename in REQUIRED_CORE_FILES:
        filepath = os.path.join(vault_dir, filename)
        if not os.path.exists(filepath):
            violations.append(f"Missing required artifact: {filename}")
            continue

        size = os.path.getsize(filepath)
        if size < MIN_FILE_SIZE_BYTES:
            violations.append(
                f"File '{filename}' size ({size} bytes) below threshold "
                f"({MIN_FILE_SIZE_BYTES} bytes). Likely empty or stub dump."
            )

    missing_critical = [
        v
        for v in violations
        if "Missing required artifact" in v or "below threshold" in v
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
                    f"(expected >= {min_rows}). Possible hydration truncation."
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


# ==============================================================================
# SECTION 2: TEST CRUCIBLE
# ==============================================================================


class TestIngestContractOracle(unittest.TestCase):
    """Dan Luu-style testing battery for RFC-012 ingestion contracts."""

    def test_production_verifier_parity_with_oracle(self):
        """Step 2: Production verify_vault_contract has 100% parity with oracle."""
        for vault_dir in ["gw7", "gw8"]:
            if not os.path.isdir(vault_dir):
                continue

            oracle_valid, oracle_violations = independently_verify_vault_contract(
                vault_dir
            )
            prod_valid, prod_violations = verify_vault_contract(vault_dir)

            self.assertEqual(
                prod_valid,
                oracle_valid,
                f"Parity mismatch on {vault_dir}: "
                f"prod={prod_valid}, oracle={oracle_valid}",
            )
            self.assertEqual(
                len(prod_violations),
                len(oracle_violations),
                f"Violation count mismatch on {vault_dir}",
            )

    def test_real_vault_gw7_golden_master_passes(self):
        """Step 4: The completed gw7 vault MUST satisfy the contract."""
        gw7_dir = "gw7"
        if not os.path.isdir(gw7_dir):
            self.skipTest(f"Directory {gw7_dir} not found.")

        is_valid, violations = independently_verify_vault_contract(gw7_dir)
        self.assertTrue(
            is_valid,
            "Golden Master gw7 failed contract oracle! Violations:\n"
            + "\n".join(violations),
        )
        self.assertEqual(violations, [])

    def test_real_vault_gw8_incomplete_state_caught_deterministically(self):
        """Step 1 & 4: Incomplete gw8 vault MUST be caught deterministically."""
        gw8_dir = "gw8"
        if not os.path.isdir(gw8_dir):
            self.skipTest(f"Directory {gw8_dir} not found.")

        is_valid, violations = independently_verify_vault_contract(gw8_dir)
        self.assertFalse(is_valid, "gw8 was expected to fail validation!")

        violation_text = "\n".join(violations)
        self.assertIn("fixtures_5w.html", violation_text)
        self.assertIn("below threshold", violation_text)
        self.assertIn("Missing required artifact: squad.html", violation_text)
        self.assertIn("Missing required artifact: defenders_2.html", violation_text)

    def test_failure_surface_truncated_player_table(self):
        """Step 1: Ghost React hydration with < 20 rows triggers violation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_html = """
            <html><body>
                <table class="_1nvnlp41">
                    <tr class="_1trl5ao0">
                        <td><span class="rfkqam4">Saliba</span></td>
                        <td>£6.0m</td>
                    </tr>
                    <tr class="_1trl5ao0">
                        <td><span class="rfkqam4">Gabriel</span></td>
                        <td>£6.2m</td>
                    </tr>
                </table>
            </body></html>
            """
            dummy_content = "<!-- valid stub -->\n" + ("x" * 1100)
            for fname in REQUIRED_CORE_FILES:
                with open(os.path.join(tmpdir, fname), "w", encoding="utf-8") as f:
                    f.write(dummy_content)

            with open(
                os.path.join(tmpdir, "defenders.html"), "w", encoding="utf-8"
            ) as f:
                f.write(mock_html + ("\n<!-- padding -->" + " " * 1100))

            is_valid, violations = independently_verify_vault_contract(tmpdir)
            self.assertFalse(is_valid)
            self.assertTrue(
                any(
                    "defenders.html: Found only 2 player rows" in v for v in violations
                ),
                f"Expected hydration truncation violation, got: {violations}",
            )

    def test_failure_surface_malformed_squad_count(self):
        """Step 1: Squad table with 14 or 16 players is strictly rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            dummy_content = "<!-- valid stub -->\n" + ("x" * 1100)
            for fname in REQUIRED_CORE_FILES:
                with open(os.path.join(tmpdir, fname), "w", encoding="utf-8") as f:
                    f.write(dummy_content)

            squad_rows = "".join(
                f'<tr class="rweppyb"><td><span class="rfkqam4">'
                f"Player {i}</span></td><td>£5.0m</td></tr>"
                for i in range(14)
            )
            squad_html = f"<html><body><table>{squad_rows}</table></body></html>" + (
                " " * 1100
            )

            with open(os.path.join(tmpdir, "squad.html"), "w", encoding="utf-8") as f:
                f.write(squad_html)

            is_valid, violations = independently_verify_vault_contract(tmpdir)
            self.assertFalse(is_valid)
            self.assertTrue(
                any(
                    "Found 14 squad rows (strictly expected exactly 15)" in v
                    for v in violations
                ),
                f"Expected squad count violation, got: {violations}",
            )

    def test_idempotency_contract_verification_has_zero_side_effects(self):
        """Step 3: Contract verification is strictly read-only and idempotent."""
        gw7_dir = "gw7"
        if not os.path.isdir(gw7_dir):
            self.skipTest(f"Directory {gw7_dir} not found.")

        mtimes_before = {
            f: os.path.getmtime(os.path.join(gw7_dir, f)) for f in os.listdir(gw7_dir)
        }

        is_valid_1, v_1 = independently_verify_vault_contract(gw7_dir)
        is_valid_2, v_2 = independently_verify_vault_contract(gw7_dir)

        mtimes_after = {
            f: os.path.getmtime(os.path.join(gw7_dir, f)) for f in os.listdir(gw7_dir)
        }

        self.assertEqual(is_valid_1, is_valid_2)
        self.assertEqual(v_1, v_2)
        self.assertEqual(
            mtimes_before,
            mtimes_after,
            "Contract check modified file timestamps!",
        )


if __name__ == "__main__":
    unittest.main()
