"""
Injury Exclusion & Squad-Page Status Reconciliation (Dan Luu Test Battery)
=========================================================================

Target law: **an injured player must never reach the solver pool.**

The market tables (goalkeepers/defenders/midfielders/forwards.csv) and the
FPL squad page (squad.csv) are independent scrapes that can disagree.
Production RUD (gw9, João Pedro): the squad page flagged a current-squad
player as INJURY while the market table still read OK, so the legacy
market-only INJURY purge let him into the pool and the Chimera drafted him
into the starting XI.

`forge_cauldron` therefore reconciles squad-page status into the pool by
(Surname, Position) using the MAX-severity law (OK < DOUBT < INJURY, never
downgrade), and only then purges INJURY.

Battery (Dan Luu principles):
  1. Pure unit test of the severity ladder (independent re-derivation).
  2. Structured synthetic vaults: every contradiction edge case.
  3. Real-vault integration on an immutable copy of gw9 (all four
     status-quadrants occur naturally there), verifying Layer-1 files are
     never mutated.
"""

import os
import shutil
import tempfile
import unittest
from typing import Dict, List, Tuple

import pandas as pd

from fpl_dominator.forge_cauldron import _max_severity_status, forge_cauldron

MARKET_HEADER = ["Surname", "Team", "Position", "Price", "TP", "Status"]
SQUAD_HEADER = ["Surname", "Team", "Position", "CP", "SP", "PP", "Status"]
ENRICHED_NAME = "fpl_master_database_enriched.csv"

# (price, tp) fills that keep the synthetic grids deterministic.
_DEFAULT_PRICE = 5.0
_DEFAULT_TP = 20


def _market_row(name: str, team: str, position: str, status: str) -> List[object]:
    return [name, team, position, _DEFAULT_PRICE, _DEFAULT_TP, status]


def _squad_row(name: str, team: str, position: str, status: str) -> List[object]:
    return [name, team, position, 5.0, 5.0, 5.0, status]


def _write_csv(path: str, header: List[str], rows: List[List[object]]) -> None:
    df = pd.DataFrame(rows, columns=header) if rows else pd.DataFrame(columns=header)
    df.to_csv(path, index=False)


def _synthetic_vault(
    base_dir: str,
    market_rows: Dict[str, List[Tuple[str, str, str]]],
    squad_rows: List[List[object]],
    write_squad: bool = True,
) -> str:
    """Forge a minimal 4-position vault. `market_rows` maps 'GKP'/'DEF'/'MID'/'FWD'
    to (name, team, status) triples — the position comes from the key itself."""
    position_files = {
        "GKP": "goalkeepers.csv",
        "DEF": "defenders.csv",
        "MID": "midfielders.csv",
        "FWD": "forwards.csv",
    }
    for position, filename in position_files.items():
        rows = [
            _market_row(name, team, position, status)
            for name, team, status in market_rows.get(position, [])
        ]
        _write_csv(os.path.join(base_dir, filename), MARKET_HEADER, rows)

    if write_squad:
        _write_csv(os.path.join(base_dir, "squad.csv"), SQUAD_HEADER, squad_rows)
    return base_dir


def _pool(enriched_path: str) -> pd.DataFrame:
    if not os.path.exists(enriched_path):
        return pd.DataFrame()
    return pd.read_csv(enriched_path)


class TestMaxSeverityLadder(unittest.TestCase):
    """Dan Luu Principle 2: independent re-derivation of the severity law."""

    def test_full_3x3_matrix(self) -> None:
        # The ladder must be commutative, idempotent, and pick max severity.
        expected = {
            ("OK", "OK"): "OK",
            ("OK", "DOUBT"): "DOUBT",
            ("OK", "INJURY"): "INJURY",
            ("DOUBT", "OK"): "DOUBT",
            ("DOUBT", "DOUBT"): "DOUBT",
            ("DOUBT", "INJURY"): "INJURY",
            ("INJURY", "OK"): "INJURY",
            ("INJURY", "DOUBT"): "INJURY",
            ("INJURY", "INJURY"): "INJURY",
        }
        for (a, b), want in expected.items():
            self.assertEqual(_max_severity_status(a, b), want, f"({a},{b})")
            self.assertEqual(_max_severity_status(b, a), want, f"({b},{a})")

    def test_unknown_token_yields_to_known(self) -> None:
        # A malformed status can never mask a genuine injury signal.
        self.assertEqual(_max_severity_status("GHOST", "INJURY"), "INJURY")
        self.assertEqual(_max_severity_status("INJURY", "GHOST"), "INJURY")
        self.assertEqual(_max_severity_status("GHOST", "DOUBT"), "DOUBT")

    def test_two_unknown_tokens_return_second(self) -> None:
        # Degenerate case: no severity info at all — document the fallback.
        self.assertEqual(_max_severity_status("ALPHA", "BETA"), "BETA")


class TestInjuryExclusionSynthetic(unittest.TestCase):
    """Structured synthetic vaults — every contradiction edge case."""

    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp(prefix="bamf-injury-test-")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self) -> pd.DataFrame:
        ok = forge_cauldron(self.tmp)
        self.assertTrue(ok, "forge_cauldron reported failure")
        return _pool(os.path.join(self.tmp, ENRICHED_NAME))

    def test_squad_injury_overrides_market_ok(self) -> None:
        # THE gw9 João Pedro case: the money-maker the market still calls healthy.
        _synthetic_vault(
            self.tmp,
            market_rows={"FWD": [("João Pedro", "Chelsea", "OK")]},
            squad_rows=[_squad_row("João Pedro", "Chelsea", "FWD", "INJURY")],
        )
        pool = self._run()
        self.assertEqual(list(pool["Surname"]), [], "injured player escaped the purge")

    def test_never_downgrade_market_injury_to_squad_ok(self) -> None:
        _synthetic_vault(
            self.tmp,
            market_rows={"MID": [("Saka", "Arsenal", "INJURY")]},
            squad_rows=[_squad_row("Saka", "Arsenal", "MID", "OK")],
        )
        pool = self._run()
        self.assertNotIn("Saka", list(pool["Surname"]))

    def test_doubt_propagates_but_remains_eligible(self) -> None:
        # DOUBT is a downgrade FROM the squad page but an UPGRADE on the pool:
        # the player stays eligible (only INJURY purges), and the status is recorded.
        _synthetic_vault(
            self.tmp,
            market_rows={"DEF": [("Calafiori", "Arsenal", "OK")]},
            squad_rows=[_squad_row("Calafiori", "Arsenal", "DEF", "DOUBT")],
        )
        pool = self._run()
        row = pool[pool["Surname"] == "Calafiori"]
        self.assertEqual(len(row), 1)
        self.assertEqual(row.iloc[0]["Status"], "DOUBT")

    def test_market_only_injury_still_purged(self) -> None:
        # Legacy law regression: market-flagged injury with no squad row at all.
        _synthetic_vault(
            self.tmp,
            market_rows={
                "GKP": [("Dubravka", "Spurs", "INJURY"), ("Raya", "Arsenal", "OK")]
            },
            squad_rows=[],
        )
        pool = self._run()
        self.assertNotIn("Dubravka", list(pool["Surname"]))
        self.assertIn("Raya", list(pool["Surname"]))

    def test_squad_member_absent_from_market_is_ignored(self) -> None:
        # Squad page lists a player the market scrape never saw: no crash,
        # no phantom row, healthy market players untouched.
        _synthetic_vault(
            self.tmp,
            market_rows={"FWD": [("Haaland", "Man City", "OK")]},
            squad_rows=[_squad_row("Phantom", "Chelsea", "FWD", "INJURY")],
        )
        pool = self._run()
        self.assertEqual(list(pool["Surname"]), ["Haaland"])

    def test_no_squad_file_legacy_behavior(self) -> None:
        _synthetic_vault(
            self.tmp,
            market_rows={
                "FWD": [("A", "X", "OK")],
                "MID": [("B", "Y", "INJURY")],
            },
            squad_rows=[],
            write_squad=False,
        )
        pool = self._run()
        self.assertEqual(list(pool["Surname"]), ["A"])

    def test_unknown_status_token_cannot_mask_injury(self) -> None:
        _synthetic_vault(
            self.tmp,
            market_rows={"MID": [("C", "Z", "GLITCHED")]},
            squad_rows=[_squad_row("C", "Z", "MID", "INJURY")],
        )
        pool = self._run()
        self.assertEqual(list(pool["Surname"]), [])

    def test_ppm_still_computed_for_survivors(self) -> None:
        # The enrichment step must keep working alongside reconciliation.
        _synthetic_vault(
            self.tmp,
            market_rows={"FWD": [("Haaland", "Man City", "OK")]},
            squad_rows=[_squad_row("Haaland", "Man City", "FWD", "OK")],
        )
        pool = self._run()
        self.assertEqual(pool.iloc[0]["PPM"], round(20 / 5.0, 2))


class TestGw9RealVaultIntegration(unittest.TestCase):
    """Dan Luu Principle 4: the real gw9 vault. All four status quadrants
    occur naturally there:
      João Pedro (FWD): market OK,  squad INJURY  -> must be EXCLUDED
      Saka (MID):       market OK,  squad INJURY  -> must be EXCLUDED
      Calafiori (DEF):  market OK,  squad DOUBT   -> stays, upgraded to DOUBT
      Thomas (DEF):     market OK,  squad DOUBT   -> stays, upgraded to DOUBT
      De Cuyper (DEF):  market OK,  squad OK      -> stays, OK
    Runs on a throwaway COPY: Layer-1 vault files are immutable ground truth.
    """

    REQUIRED_FILES = (
        "goalkeepers.csv",
        "defenders.csv",
        "midfielders.csv",
        "forwards.csv",
        "squad.csv",
        ENRICHED_NAME,
    )
    ORIGINAL_POOL_SIZE = 240  # 4 market tables x 60 players, zero market INJURY rows
    EXPECTED_POOL_SIZE = 238  # 240 - João Pedro - Saka (squad-page INJURY upgrades)

    @classmethod
    def setUpClass(cls) -> None:
        if not all(os.path.exists(f"gw9/{f}") for f in cls.REQUIRED_FILES):
            raise unittest.SkipTest(
                "Missing gw9 vault artifacts for injury integration"
            )
        cls.tmp = tempfile.mkdtemp(prefix="bamf-gw9-injury-")
        cls.copy_dir = os.path.join(cls.tmp, "gw9")
        shutil.copytree("gw9", cls.copy_dir)
        cls.original_enriched = pd.read_csv(f"gw9/{ENRICHED_NAME}")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _run_on_copy(self) -> pd.DataFrame:
        ok = forge_cauldron(self.copy_dir)
        self.assertTrue(ok, "forge_cauldron failed on real gw9 copy")
        return _pool(os.path.join(self.copy_dir, ENRICHED_NAME))

    def test_injured_current_squad_players_excluded(self) -> None:
        pool = self._run_on_copy()
        surnames = set(pool["Surname"])
        self.assertNotIn("João Pedro", surnames)
        self.assertNotIn("Saka", surnames)

    def test_no_injury_status_leaks_into_pool(self) -> None:
        pool = self._run_on_copy()
        self.assertNotIn("INJURY", set(pool["Status"]), "INJURY row survived the purge")

    def test_doubt_players_upgraded_but_eligible(self) -> None:
        pool = self._run_on_copy()
        for name in ("Calafiori", "Thomas"):
            row = pool[pool["Surname"] == name]
            self.assertEqual(len(row), 1, f"{name} missing from pool")
            self.assertEqual(row.iloc[0]["Status"], "DOUBT")

    def test_clean_player_untouched(self) -> None:
        pool = self._run_on_copy()
        row = pool[pool["Surname"] == "De Cuyper"]
        self.assertEqual(len(row), 1)
        self.assertEqual(row.iloc[0]["Status"], "OK")

    def test_pool_size_drops_by_exactly_the_reconciled_injuries(self) -> None:
        pool = self._run_on_copy()
        self.assertEqual(len(pool), self.EXPECTED_POOL_SIZE)
        self.assertEqual(len(self.original_enriched), self.ORIGINAL_POOL_SIZE)

    def test_original_vault_untouched(self) -> None:
        # Layer-1 immutability: the committed gw9 vault must be byte-identical.
        _ = self._run_on_copy()
        after = pd.read_csv(f"gw9/{ENRICHED_NAME}")
        pd.testing.assert_frame_equal(self.original_enriched, after)


if __name__ == "__main__":
    unittest.main()
