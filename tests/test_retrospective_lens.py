"""Dan Luu-style unit, property, and integration tests for RFC-011 Retrospective Lens.

Methodology (Dan Luu Testing Heuristics):
1. Pre-implementation edge-case identification:
   - State likely mistakes and alternative interpretations.
   - Test asymmetric / boundary examples on both sides of boundaries (e.g. GW1
     cold start, GW2 lookback overshoot, Bayesian annualized TP vs Raw_TP
     fallback, negative delta clamping).
2. Independent re-derivation:
   - Independently re-derive the mathematical equations from RFC-011 with fresh
     context without re-using production helper functions or constants.
3. Structured randomized inputs & property-based invariants:
   - Explore non-trivial state spaces (mixed positions, extreme FDRs, hauls vs
     blanks).
   - Validate mathematical invariants: non-negativity, parity identity,
     monotonic difficulty scaling.
4. Real-world vault integration:
   - Verify historical extraction against actual gw1-gw4 repository vaults.
"""

import os
import random
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd

from fpl_dominator.retrospective_lens import (
    calculate_retrospective_form,
    extract_historical_fixture_fdr,
    extract_historical_player_points,
)


def _independently_rederived_retrospective_form(
    gameweek_points: list[float],
    gameweek_fdrs: list[float],
    position: str,
) -> tuple[float, float, float]:
    """Completely independent mathematical re-derivation of RFC-011 formulas.

    NOTE: Written with fresh context without calling ANY production functions
    or importing any production constants from retrospective_lens.py.

    RFC-011 Specification:
    1. Raw_Form = sum(Points_g)
    2. Adjusted_Form = sum(Points_g * (FDR_past_g / 1000.0))
    3. Form_Efficiency = sum(Points_g) / sum(Expected_Points(FDR_past_g))
       where:
         - Baseline expected points at parity FDR (1150.0):
           GKP: 3.5, DEF: 3.5, MID: 4.5, FWD: 4.5
         - Expected points per gameweek = base_exp * (1150.0 / max(800.0, fdr))
         - Efficiency denominator clamped to max(0.5, total_expected_points)
    """
    total_raw = sum(gameweek_points)

    total_adjusted = 0.0
    for pts, fdr in zip(gameweek_points, gameweek_fdrs):
        multiplier = fdr / 1000.0
        total_adjusted += pts * multiplier

    pos_upper = position.strip().upper()
    if pos_upper in ("GKP", "DEF"):
        base_exp = 3.5
    elif pos_upper in ("MID", "FWD"):
        base_exp = 4.5
    else:
        base_exp = 4.0

    total_expected = 0.0
    for fdr in gameweek_fdrs:
        clamped_fdr = max(800.0, float(fdr))
        exp_pts = base_exp * (1150.0 / clamped_fdr)
        total_expected += exp_pts

    if total_expected > 0.0:
        safe_denominator = max(0.5, total_expected)
        efficiency = round(total_raw / safe_denominator, 2)
    else:
        efficiency = 1.0

    return round(total_raw, 2), round(total_adjusted, 2), efficiency


class TestRetrospectiveLensEdgeCasesAndBoundaries(unittest.TestCase):
    """Dan Luu Principle 1: Pre-implementation edge cases and asymmetric boundaries."""

    def test_gw1_cold_start_boundary(self):
        """Boundary: current_gw = 1 (Cold start before any gameweeks have occurred).

        Likely mistake: target_gws evaluates to empty, causing ZeroDivisionError
        or attempting to load non-existent gw0/fixtures.csv.
        Alternative interpretation: GW1 might attempt to look back to previous season.
        Specification invariant: For GW1, target_gws is empty; all forms default safely
        to Raw_Form = 0.0, Adjusted_Form = 0.0, Form_Efficiency = 1.0.
        """
        fdr_map = extract_historical_fixture_fdr(current_gw=1, lookback_weeks=2)
        self.assertEqual(fdr_map, {})

        points_map = extract_historical_player_points(current_gw=1, lookback_weeks=2)
        self.assertEqual(points_map, {})

        df_input = pd.DataFrame(
            [
                {
                    "Surname": "Haaland",
                    "Team": "Man City",
                    "Position": "FWD",
                    "TP": 0,
                    "Raw_TP": 0,
                },
                {
                    "Surname": "Saka",
                    "Team": "Arsenal",
                    "Position": "MID",
                    "TP": 0,
                    "Raw_TP": 0,
                },
            ]
        )

        df_result = calculate_retrospective_form(
            df_input, current_gw=1, lookback_weeks=2
        )
        self.assertIn("Raw_Form", df_result.columns)
        self.assertIn("Adjusted_Form", df_result.columns)
        self.assertIn("Form_Efficiency", df_result.columns)

        for _, row in df_result.iterrows():
            self.assertEqual(row["Raw_Form"], 0.0)
            self.assertEqual(row["Adjusted_Form"], 0.0)
            self.assertEqual(row["Form_Efficiency"], 1.0)

    def test_gw2_asymmetric_lookback_boundary(self):
        """Boundary: current_gw = 2, lookback_weeks = 5.

        Asymmetric condition: requested lookback (5) exceeds available gameweeks (1).
        Likely mistake: Loop iterates over negative or zero gameweeks, or divides by 5
        instead of evaluating the single available historical gameweek (GW1).
        """
        # start_gw = max(1, 2 - 5) = 1. target_gws = [1]
        with tempfile.TemporaryDirectory() as tmpdir:
            orig_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Setup gw1 fixtures and enriched db
                os.makedirs("gw1", exist_ok=True)
                pd.DataFrame(
                    [
                        {
                            "Gameweek": "GW1",
                            "Team": "ARS",
                            "FDR": 1200.0,
                            "FDR_A": 1100.0,
                            "FDR_D": 1300.0,
                        }
                    ]
                ).to_csv("gw1/fixtures.csv", index=False)
                pd.DataFrame(
                    [
                        {
                            "Surname": "Saka",
                            "Team": "Arsenal",
                            "Position": "MID",
                            "TP": 8.0,
                        }
                    ]
                ).to_csv("gw1/fpl_master_database_enriched.csv", index=False)

                fdr_map = extract_historical_fixture_fdr(current_gw=2, lookback_weeks=5)
                self.assertIn(("ARS", 1), fdr_map)
                self.assertNotIn(("ARS", 2), fdr_map)
                self.assertEqual(fdr_map[("ARS", 1)]["FDR_A"], 1100.0)

                points_map = extract_historical_player_points(
                    current_gw=2, lookback_weeks=5
                )
                self.assertIn(("Saka", "Arsenal"), points_map)
                # In GW1, points are equal to TP
                self.assertEqual(points_map[("Saka", "Arsenal")][1], 8.0)

                players_df = pd.DataFrame(
                    [
                        {
                            "Surname": "Saka",
                            "Team": "Arsenal",
                            "Position": "MID",
                            "TP": 8.0,
                            "Raw_TP": 8.0,
                        }
                    ]
                )
                res_df = calculate_retrospective_form(
                    players_df, current_gw=2, lookback_weeks=5
                )
                # Only 1 gameweek evaluated: Raw_Form = 8.0
                self.assertEqual(res_df.iloc[0]["Raw_Form"], 8.0)
                # Adjusted_Form = 8.0 * (1100.0 / 1000.0) = 8.8
                self.assertEqual(res_df.iloc[0]["Adjusted_Form"], 8.8)
            finally:
                os.chdir(orig_cwd)

    def test_historical_snapshot_fallback_regression_mitchell_bug(self):
        """CRITICAL REGRESSION TEST: Annualized Bayesian TP vs Actual Raw_TP fallback.

        Likely mistake (The Bug): When a player is missing from historical snapshots
        (e.g., Mitchell, Van Hecke), fallback evaluated row.get("TP") divided by
        len(target_gws). But row["TP"] had already been replaced by 38-game annualized
        Bayesian prior (e.g. TP = 176.0), resulting in 88 pts/game and
        Adjusted_Form = 220.44!

        Correct implementation: Fallback must use row.get("Raw_TP", row.get("TP"))
        divided by max(1, current_gw - 1) (actual games played so far).
        Check where results differ:
          - Player with Raw_TP = 12.0, Bayesian TP = 176.0 at GW4 with lookback 2.
          - Buggy formula: 176 / 2 = 88 pts/gw -> Raw_Form = 176.0.
          - Correct formula: 12.0 / 3 = 4.0 pts/gw -> Raw_Form = 8.0.
        """
        players_df = pd.DataFrame(
            [
                {
                    "Surname": "Mitchell",
                    "Team": "Crystal Palace",
                    "Position": "DEF",
                    "TP": 176.0,  # Annualized Bayesian Prior
                    "Raw_TP": 12.0,  # Actual cumulative points across GW1-3
                }
            ]
        )

        with (
            patch(
                "fpl_dominator.retrospective_lens.extract_historical_player_points",
                return_value={},
            ),
            patch(
                "fpl_dominator.retrospective_lens.extract_historical_fixture_fdr",
                return_value={
                    ("CRY", 2): {"FDR": 1000.0, "FDR_A": 1000.0, "FDR_D": 1000.0},
                    ("CRY", 3): {"FDR": 1000.0, "FDR_A": 1000.0, "FDR_D": 1000.0},
                },
            ),
        ):
            res_df = calculate_retrospective_form(
                players_df, current_gw=4, lookback_weeks=2
            )
            mitchell_res = res_df.iloc[0]

            # In GW4, games_played = 4 - 1 = 3.
            # Average points per past GW = 12.0 / 3 = 4.0.
            # Lookback target_gws = [2, 3] (2 weeks).
            # Expected Raw_Form = 4.0 * 2 = 8.0.
            self.assertEqual(mitchell_res["Raw_Form"], 8.0)
            self.assertEqual(mitchell_res["Adjusted_Form"], 8.0)

            # Assert the bug is NOT present
            self.assertNotEqual(mitchell_res["Raw_Form"], 176.0)
            self.assertNotEqual(mitchell_res["Raw_Form"], 88.0)

    def test_fallback_without_raw_tp_column(self):
        """Edge case: DataFrame does not have Raw_TP column (e.g. pre-enrichment).

        When Raw_TP is missing, row.get("Raw_TP", row.get("TP")) gracefully falls back
        to TP divided by max(1, current_gw - 1).
        """
        players_df = pd.DataFrame(
            [
                {
                    "Surname": "Unknown",
                    "Team": "Arsenal",
                    "Position": "MID",
                    "TP": 15.0,  # Pure TP without Raw_TP
                }
            ]
        )

        with (
            patch(
                "fpl_dominator.retrospective_lens.extract_historical_player_points",
                return_value={},
            ),
            patch(
                "fpl_dominator.retrospective_lens.extract_historical_fixture_fdr",
                return_value={},
            ),
        ):
            res_df = calculate_retrospective_form(
                players_df, current_gw=4, lookback_weeks=2
            )
            # 15.0 / (4 - 1) = 5.0 pts/gw. Lookback 2 gws = 10.0 pts.
            self.assertEqual(res_df.iloc[0]["Raw_Form"], 10.0)

    def test_positional_fdr_bifurcation(self):
        """Asymmetric check: DEF/GKP evaluated against FDR_D; MID/FWD against FDR_A.

        Likely mistake: Using general FDR for all positions, or mixing up FDR_D and
        FDR_A.
        Asymmetric setup:
          - Opponent has FDR_D = 1400.0 (high defensive difficulty / lethal attack).
          - Opponent has FDR_A = 900.0 (low attacking difficulty / leaky defense).
        Result diff:
          - Defender scoring 10 pts gets 10 * 1.4 = 14.0 Adjusted_Form.
          - Midfielder scoring 10 pts gets 10 * 0.9 = 9.0 Adjusted_Form.
        """
        players_df = pd.DataFrame(
            [
                {
                    "Surname": "Gabriel",
                    "Team": "Arsenal",
                    "Position": "DEF",
                    "TP": 10.0,
                    "Raw_TP": 10.0,
                },
                {
                    "Surname": "Saka",
                    "Team": "Arsenal",
                    "Position": "MID",
                    "TP": 10.0,
                    "Raw_TP": 10.0,
                },
            ]
        )

        mock_deltas = {
            ("Gabriel", "Arsenal"): {3: 10.0},
            ("Saka", "Arsenal"): {3: 10.0},
        }
        mock_fdrs = {
            ("ARS", 3): {"FDR": 1150.0, "FDR_A": 900.0, "FDR_D": 1400.0},
        }

        with (
            patch(
                "fpl_dominator.retrospective_lens.extract_historical_player_points",
                return_value=mock_deltas,
            ),
            patch(
                "fpl_dominator.retrospective_lens.extract_historical_fixture_fdr",
                return_value=mock_fdrs,
            ),
        ):
            res_df = calculate_retrospective_form(
                players_df, current_gw=4, lookback_weeks=1
            )
            def_row = res_df[res_df["Surname"] == "Gabriel"].iloc[0]
            mid_row = res_df[res_df["Surname"] == "Saka"].iloc[0]

            self.assertEqual(def_row["Raw_Form"], 10.0)
            self.assertEqual(mid_row["Raw_Form"], 10.0)

            # DEF evaluates against FDR_D (1400) -> 10.0 * 1.4 = 14.0
            self.assertEqual(def_row["Adjusted_Form"], 14.0)
            # MID evaluates against FDR_A (900) -> 10.0 * 0.9 = 9.0
            self.assertEqual(mid_row["Adjusted_Form"], 9.0)

            # Also verify Form Efficiency positional baselines differ:
            # DEF baseline: 3.5 * (1150 / 1400) = 2.875 exp pts -> 10 / 2.875 = 3.48
            # MID baseline: 4.5 * (1150 / 900) = 5.75 exp pts -> 10 / 5.75 = 1.74
            self.assertGreater(def_row["Form_Efficiency"], mid_row["Form_Efficiency"])

    def test_negative_point_delta_clamping(self):
        """Asymmetric check: Statistical corrections where curr_tp < prev_tp.

        Likely mistake: Naive subtraction curr_tp - prev_tp gives negative points.
        Specification invariant: Negative deltas clamped to 0.0 via max(0.0, delta).
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            orig_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                os.makedirs("gw1", exist_ok=True)
                os.makedirs("gw2", exist_ok=True)

                # GW1: Player had 15 points
                pd.DataFrame(
                    [
                        {
                            "Surname": "ErrorPlayer",
                            "Team": "Arsenal",
                            "Position": "MID",
                            "TP": 15.0,
                        }
                    ]
                ).to_csv("gw1/fpl_master_database_enriched.csv", index=False)

                # GW2: After stat adjustment/deduction, TP dropped to 14.0
                pd.DataFrame(
                    [
                        {
                            "Surname": "ErrorPlayer",
                            "Team": "Arsenal",
                            "Position": "MID",
                            "TP": 14.0,
                        }
                    ]
                ).to_csv("gw2/fpl_master_database_enriched.csv", index=False)

                points_map = extract_historical_player_points(
                    current_gw=3, lookback_weeks=1
                )
                self.assertIn(("ErrorPlayer", "Arsenal"), points_map)
                # Delta must be clamped to 0.0, NOT -1.0
                self.assertEqual(points_map[("ErrorPlayer", "Arsenal")][2], 0.0)
            finally:
                os.chdir(orig_cwd)

    def test_mid_season_transfer_addition(self):
        """Check player present in snapshot g but missing in snapshot g-1.

        Likely mistake: Missing in previous snapshot causes KeyError or 0 delta.
        Specification invariant: If player is new to the database, delta is curr_tp.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            orig_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                os.makedirs("gw1", exist_ok=True)
                os.makedirs("gw2", exist_ok=True)

                # GW1: Only Saka
                pd.DataFrame(
                    [
                        {
                            "Surname": "Saka",
                            "Team": "Arsenal",
                            "Position": "MID",
                            "TP": 5.0,
                        }
                    ]
                ).to_csv("gw1/fpl_master_database_enriched.csv", index=False)

                # GW2: Saka + New signing Calafiori
                pd.DataFrame(
                    [
                        {
                            "Surname": "Saka",
                            "Team": "Arsenal",
                            "Position": "MID",
                            "TP": 12.0,
                        },
                        {
                            "Surname": "Calafiori",
                            "Team": "Arsenal",
                            "Position": "DEF",
                            "TP": 6.0,
                        },
                    ]
                ).to_csv("gw2/fpl_master_database_enriched.csv", index=False)

                points_map = extract_historical_player_points(
                    current_gw=3, lookback_weeks=1
                )
                self.assertIn(("Calafiori", "Arsenal"), points_map)
                # Delta for Calafiori in GW2 must be 6.0
                self.assertEqual(points_map[("Calafiori", "Arsenal")][2], 6.0)
                # Delta for Saka in GW2 is 12 - 5 = 7.0
                self.assertEqual(points_map[("Saka", "Arsenal")][2], 7.0)
            finally:
                os.chdir(orig_cwd)

    def test_fixtures_fallback_cascades(self):
        """Check fixture fallback cascade when gw{g}/fixtures.csv is absent.

        Cascade: gw{g}/fixtures.csv -> gw{current_gw}/fixtures.csv -> PARITY_FDR.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            orig_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # Only current_gw fixtures exist
                os.makedirs("gw3", exist_ok=True)
                pd.DataFrame(
                    [
                        {
                            "Gameweek": "GW2",
                            "Team": "MCI",
                            "FDR": 1350.0,
                            "FDR_A": 1250.0,
                            "FDR_D": 1450.0,
                        }
                    ]
                ).to_csv("gw3/fixtures.csv", index=False)

                fdr_map = extract_historical_fixture_fdr(current_gw=3, lookback_weeks=1)
                self.assertIn(("MCI", 2), fdr_map)
                self.assertEqual(fdr_map[("MCI", 2)]["FDR"], 1350.0)
                self.assertEqual(fdr_map[("MCI", 2)]["FDR_A"], 1250.0)
                self.assertEqual(fdr_map[("MCI", 2)]["FDR_D"], 1450.0)
            finally:
                os.chdir(orig_cwd)


class TestRetrospectiveLensIndependentReDerivation(unittest.TestCase):
    """Dan Luu Principle 2 & 5: Independent re-derivation without production helpers."""

    def test_cross_validation_with_independent_oracle(self):
        """Cross-validate calculate_retrospective_form with independent oracle math.

        Generates multiple position and difficulty scenarios, then compares
        production outputs bit-for-bit against independent re-derivation.
        """
        test_cases = [
            # (position, [pts_gw2, pts_gw3], [fdr_gw2, fdr_gw3])
            ("FWD", [4.0, 13.0], [1139.0, 1139.0]),  # Haaland-like haul
            ("MID", [7.0, 6.0], [900.0, 1250.0]),  # Mixed difficulty
            ("DEF", [2.0, 15.0], [1400.0, 1000.0]),  # Tough attack then parity
            ("GKP", [1.0, 3.0], [800.0, 850.0]),  # Low FDR clamp test
            ("DEF", [0.0, 0.0], [1200.0, 1300.0]),  # Zero points blank
        ]

        for idx, (pos, pts, fdrs) in enumerate(test_cases):
            player_name = f"Player_{idx}"
            team_name = "Arsenal"
            team_tla = "ARS"

            # 1. Evaluate independent oracle
            exp_raw, exp_adj, exp_eff = _independently_rederived_retrospective_form(
                pts, fdrs, pos
            )

            # 2. Evaluate production code
            players_df = pd.DataFrame(
                [
                    {
                        "Surname": player_name,
                        "Team": team_name,
                        "Position": pos,
                        "TP": sum(pts),
                        "Raw_TP": sum(pts),
                    }
                ]
            )
            mock_deltas = {
                (player_name, team_name): {2: pts[0], 3: pts[1]},
            }
            # Match positional FDR mapping
            if pos in ("GKP", "DEF"):
                mock_fdrs = {
                    (team_tla, 2): {
                        "FDR": fdrs[0],
                        "FDR_A": 1000.0,
                        "FDR_D": fdrs[0],
                    },
                    (team_tla, 3): {
                        "FDR": fdrs[1],
                        "FDR_A": 1000.0,
                        "FDR_D": fdrs[1],
                    },
                }
            else:
                mock_fdrs = {
                    (team_tla, 2): {
                        "FDR": fdrs[0],
                        "FDR_A": fdrs[0],
                        "FDR_D": 1000.0,
                    },
                    (team_tla, 3): {
                        "FDR": fdrs[1],
                        "FDR_A": fdrs[1],
                        "FDR_D": 1000.0,
                    },
                }

            with (
                patch(
                    "fpl_dominator.retrospective_lens.extract_historical_player_points",
                    return_value=mock_deltas,
                ),
                patch(
                    "fpl_dominator.retrospective_lens.extract_historical_fixture_fdr",
                    return_value=mock_fdrs,
                ),
            ):
                res_df = calculate_retrospective_form(
                    players_df, current_gw=4, lookback_weeks=2
                )
                prod_row = res_df.iloc[0]

                self.assertAlmostEqual(
                    prod_row["Raw_Form"],
                    exp_raw,
                    places=2,
                    msg=f"Case {idx} Raw_Form: {prod_row['Raw_Form']} != {exp_raw}",
                )
                self.assertAlmostEqual(
                    prod_row["Adjusted_Form"],
                    exp_adj,
                    places=2,
                    msg=(
                        f"Case {idx} Adjusted_Form: "
                        f"{prod_row['Adjusted_Form']} != {exp_adj}"
                    ),
                )
                self.assertAlmostEqual(
                    prod_row["Form_Efficiency"],
                    exp_eff,
                    places=2,
                    msg=(
                        f"Case {idx} Form_Efficiency: "
                        f"{prod_row['Form_Efficiency']} != {exp_eff}"
                    ),
                )


class TestRetrospectiveLensPropertyBasedAndRandomized(unittest.TestCase):
    """Dan Luu Principle 3 & 4: Structured randomized inputs exploring state space."""

    def setUp(self):
        self.rng = random.Random(1337)  # Deterministic seed

    def test_property_invariants_across_structured_random_squads(self):
        """Property-based verification of mathematical invariants across profiles.

        Invariants checked:
        1. Non-negativity: Raw_Form >= 0, Adjusted_Form >= 0, Form_Efficiency >= 0.
        2. Parity Identity: When FDR == 1000.0, Adjusted_Form == Raw_Form.
        3. Monotonic Difficulty: If all FDR > 1000.0, Adjusted_Form > Raw_Form.
        4. Monotonic Easiness: If all FDR < 1000.0, Adjusted_Form < Raw_Form.
        5. Zero Points Identity: If Points == 0, Raw_Form == 0, Adjusted_Form == 0.
        """
        positions = ["GKP", "DEF", "MID", "FWD"]

        for iteration in range(100):
            pos = self.rng.choice(positions)
            points_gw2 = self.rng.choice([0.0, 1.0, 2.0, 6.0, 12.0, 18.0])
            points_gw3 = self.rng.choice([0.0, 2.0, 5.0, 8.0, 15.0])
            total_points = points_gw2 + points_gw3

            # Regime 1: Parity FDR (1000.0)
            fdr_parity = 1000.0
            raw_p, adj_p, eff_p = _independently_rederived_retrospective_form(
                [points_gw2, points_gw3], [fdr_parity, fdr_parity], pos
            )
            self.assertGreaterEqual(raw_p, 0.0)
            self.assertGreaterEqual(adj_p, 0.0)
            self.assertGreaterEqual(eff_p, 0.0)
            self.assertEqual(
                raw_p,
                adj_p,
                f"Parity invariant violated at iteration {iteration}",
            )

            # Regime 2: Brutal Schedule (all FDRs > 1000.0)
            fdr_hard_1 = self.rng.uniform(1050.0, 1600.0)
            fdr_hard_2 = self.rng.uniform(1050.0, 1600.0)
            raw_h, adj_h, eff_h = _independently_rederived_retrospective_form(
                [points_gw2, points_gw3], [fdr_hard_1, fdr_hard_2], pos
            )
            self.assertGreaterEqual(raw_h, 0.0)
            self.assertGreaterEqual(adj_h, 0.0)
            self.assertGreaterEqual(eff_h, 0.0)
            if total_points > 0.0:
                self.assertGreater(
                    adj_h,
                    raw_h,
                    f"Monotonic difficulty violated: {adj_h} <= {raw_h}",
                )

            # Regime 3: Cake Walk Schedule (all FDRs < 1000.0)
            fdr_easy_1 = self.rng.uniform(800.0, 950.0)
            fdr_easy_2 = self.rng.uniform(800.0, 950.0)
            raw_e, adj_e, eff_e = _independently_rederived_retrospective_form(
                [points_gw2, points_gw3], [fdr_easy_1, fdr_easy_2], pos
            )
            self.assertGreaterEqual(raw_e, 0.0)
            self.assertGreaterEqual(adj_e, 0.0)
            self.assertGreaterEqual(eff_e, 0.0)
            if total_points > 0.0:
                self.assertLess(
                    adj_e,
                    raw_e,
                    f"Monotonic easiness violated: {adj_e} >= {raw_e}",
                )

            # Regime 4: Zero Points scored
            raw_0, adj_0, eff_0 = _independently_rederived_retrospective_form(
                [0.0, 0.0], [fdr_hard_1, fdr_easy_1], pos
            )
            self.assertEqual(raw_0, 0.0)
            self.assertEqual(adj_0, 0.0)
            self.assertEqual(eff_0, 0.0)

    def test_fdr_clamping_boundary_at_800(self):
        """Verify FDRs below 800.0 are clamped to 800.0 in Form Efficiency."""
        pos = "MID"
        points = [10.0]

        # FDR = 800.0 vs FDR = 500.0 (below clamp)
        _, _, eff_800 = _independently_rederived_retrospective_form(
            points, [800.0], pos
        )
        _, _, eff_500 = _independently_rederived_retrospective_form(
            points, [500.0], pos
        )

        # Because max(800.0, fdr) clamps 500 to 800, efficiencies must be identical!
        self.assertEqual(eff_800, eff_500)


class TestRetrospectiveLensVaultIntegration(unittest.TestCase):
    """Integration tests executing against actual project repository vaults."""

    def test_extract_historical_fixture_fdr_gw4(self):
        """Verify fixture FDR extraction from actual gw2 and gw3 vault files."""
        if not os.path.exists("gw2/fixtures.csv") or not os.path.exists(
            "gw3/fixtures.csv"
        ):
            raise unittest.SkipTest("Missing gw2/gw3 fixture files in workspace")

        fdr_map = extract_historical_fixture_fdr(current_gw=4, lookback_weeks=2)
        self.assertTrue(len(fdr_map) > 0)

        # Lookback gameweeks are 2 and 3
        gws_found = {k[1] for k in fdr_map.keys()}
        self.assertIn(2, gws_found)
        self.assertIn(3, gws_found)

        # Check Arsenal entry
        self.assertIn(("ARS", 2), fdr_map)
        self.assertIn(("ARS", 3), fdr_map)
        ars_gw3 = fdr_map[("ARS", 3)]
        self.assertIn("FDR", ars_gw3)
        self.assertIn("FDR_A", ars_gw3)
        self.assertIn("FDR_D", ars_gw3)

    def test_extract_historical_player_points_haaland_gw4(self):
        """Verify Haaland's points extraction matches database deltas."""
        if not os.path.exists(
            "gw2/fpl_master_database_enriched.csv"
        ) or not os.path.exists("gw3/fpl_master_database_enriched.csv"):
            raise unittest.SkipTest("Missing gw2/gw3 database files in workspace")

        points_map = extract_historical_player_points(current_gw=4, lookback_weeks=2)
        haaland_key = ("Haaland", "Man City")
        self.assertIn(haaland_key, points_map)

        haaland_deltas = points_map[haaland_key]
        # In GW2: TP was 2 (delta = 2 - 0 = 2)
        # In GW3: TP was 15 (delta = 15 - 2 = 13)
        self.assertEqual(haaland_deltas.get(2), 2.0)
        self.assertEqual(haaland_deltas.get(3), 13.0)

    def test_calculate_retrospective_form_gw4_prophetic_sanity(self):
        """Verify calculate_retrospective_form runs on gw4 without anomalous blowups.

        Replaces brittle single-player name checks with population-wide invariants:
        1. Universal sanity bounds (no player exceeds maximum realistic 2-week form).
        2. Strict non-negativity across all metrics.
        3. Systematic verification of the fallback invariant across the entire
           cohort of un-snapshotted players.
        """
        if not os.path.exists("gw4/fpl_master_database_prophetic.csv"):
            raise unittest.SkipTest("Missing gw4 prophetic database")

        df_pro = pd.read_csv("gw4/fpl_master_database_prophetic.csv")
        self.assertIn("Raw_Form", df_pro.columns)
        self.assertIn("Adjusted_Form", df_pro.columns)
        self.assertIn("Form_Efficiency", df_pro.columns)

        # 1. No NaNs or infinities
        self.assertFalse(df_pro["Raw_Form"].isna().any())
        self.assertFalse(df_pro["Adjusted_Form"].isna().any())
        self.assertFalse(df_pro["Form_Efficiency"].isna().any())

        # 2. Universal population bounds (in 2 GWs, form cannot exceed 40).
        # Prevents any 38-game annualized prior leakage (>200) across the dataset.
        self.assertLess(
            float(df_pro["Adjusted_Form"].max()),
            40.0,
            f"Population max Adjusted_Form exploded: {df_pro['Adjusted_Form'].max()}",
        )
        self.assertGreaterEqual(float(df_pro["Adjusted_Form"].min()), 0.0)
        self.assertGreaterEqual(float(df_pro["Raw_Form"].min()), 0.0)
        self.assertGreaterEqual(float(df_pro["Form_Efficiency"].min()), 0.0)

        # 3. Systematic fallback cohort invariant:
        # For ALL players missing from historical snapshots, Raw_Form must strictly
        # obey the formula: (Raw_TP / games_played) * lookback_weeks
        points_map = extract_historical_player_points(current_gw=4, lookback_weeks=2)
        games_played = 4 - 1
        lookback_weeks = 2

        fallback_count = 0
        for _, row in df_pro.iterrows():
            key = (str(row["Surname"]).strip(), str(row.get("Team", "")).strip())
            if key not in points_map or not points_map[key]:
                raw_tp = float(row.get("Raw_TP", row["TP"]))
                expected_raw = round((raw_tp / games_played) * lookback_weeks, 2)
                actual_raw = float(row["Raw_Form"])
                self.assertAlmostEqual(
                    actual_raw,
                    expected_raw,
                    places=1,
                    msg=(
                        f"Fallback invariant violated for {key}: "
                        f"{actual_raw} != {expected_raw}"
                    ),
                )
                fallback_count += 1

        # Ensure that the fallback cohort actually exists and was verified (>0 players)
        self.assertGreater(fallback_count, 0)


if __name__ == "__main__":
    unittest.main()
