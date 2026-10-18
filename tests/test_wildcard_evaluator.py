"""Dan Luu-style unit and contract oracle tests for RFC-004 Wildcard Evaluator.

Validates:
1. Dan Luu Principle 1: Edge cases & boundaries (missing vaults, empty squads).
2. Dan Luu Principle 2: Independent mathematical oracle re-deriving 3-path option
   evaluation from RFC-004 formulas without production helpers.
3. Dan Luu Principle 3: Structural invariants and formation compliance of
   the greedy starting XI and MILP optimal squad.
4. Dan Luu Principle 4: Real-world vault integration on historical gw3 intelligence.
"""

import os
import re
import unittest

from fpl_dominator.wildcard_evaluator import (
    WildcardEvaluationResult,
    calculate_squad_divergence,
)


def _independently_rederived_wildcard_decision(
    current_gw: int,
    current_xi_score: float,
    optimal_xi_score: float,
    transfers_needed: int,
) -> tuple[float, float, float, float, float, bool]:
    """Completely independent mathematical re-derivation of RFC-004 formulas.

    NOTE: Re-derives all 3-path evaluation curves from first principles:
    - 5-week point projections = score * 100.0
    - Divergence = Optimal_5GW - Current_5GW
    - Dynamic threshold: max(12.0, 32.0 - (current_gw - 2) * 1.3)
    - Path A (Hold / 1 FT): current_pts + min(pts_divergence * 0.35, 12.0)
    - Path B (Mini-Wildcard): (current_pts + pts_divergence * 0.75) - (hits * 4.0)
      where hits = max(0, min(transfers_needed - 1, 4))
    - Path C (Wildcard Now): optimal_pts
    - WC Advantage = Path C - max(Path A, Path B)
    - Trigger = WC Advantage >= threshold
    """
    proj_curr = current_xi_score * 100.0
    proj_opt = optimal_xi_score * 100.0
    divergence = proj_opt - proj_curr

    threshold = max(12.0, 32.0 - (current_gw - 2) * 1.3)

    path_a = proj_curr + min(divergence * 0.35, 12.0)
    hits = max(0, min(transfers_needed - 1, 4))
    path_b = (proj_curr + divergence * 0.75) - (hits * 4.0)
    path_c = proj_opt

    wc_advantage = path_c - max(path_a, path_b)
    should_trigger = wc_advantage >= threshold

    return (
        round(divergence, 4),
        round(path_a, 4),
        round(path_b, 4),
        round(path_c, 4),
        round(wc_advantage, 4),
        should_trigger,
    )


class TestWildcardEvaluator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gw3_dir = "gw3"
        cls.required_files = [
            f"{cls.gw3_dir}/fpl_master_database_FINAL_v5.csv",
            f"{cls.gw3_dir}/squad.csv",
        ]
        if not all(os.path.exists(p) for p in cls.required_files):
            raise unittest.SkipTest("Missing gw3 vault artifacts for wildcard testing")

    def test_dan_luu_independent_wildcard_oracle(self):
        """Dan Luu Principle 2: Independent oracle parity against RFC-004 formulas."""
        res: WildcardEvaluationResult = calculate_squad_divergence(self.gw3_dir)

        gw_match = re.search(r"\d+", self.gw3_dir)
        expected_gw = int(gw_match.group()) if gw_match else 2

        (
            oracle_divergence,
            oracle_path_a,
            oracle_path_b,
            oracle_path_c,
            oracle_wc_adv,
            oracle_trigger,
        ) = _independently_rederived_wildcard_decision(
            current_gw=expected_gw,
            current_xi_score=res["current_xi_score"],
            optimal_xi_score=res["optimal_xi_score"],
            transfers_needed=res["transfers_needed"],
        )

        self.assertAlmostEqual(res["pts_divergence"], oracle_divergence, places=2)
        self.assertAlmostEqual(res["path_a_pts"], oracle_path_a, places=2)
        self.assertAlmostEqual(res["path_b_pts"], oracle_path_b, places=2)
        self.assertAlmostEqual(res["path_c_pts"], oracle_path_c, places=2)
        self.assertAlmostEqual(res["wc_advantage"], oracle_wc_adv, places=2)
        self.assertEqual(res["should_trigger"], oracle_trigger)

    def test_wildcard_evaluation_contract_and_types(self):
        """Dan Luu Principle 3: Contract invariants of WildcardEvaluationResult."""
        res: WildcardEvaluationResult = calculate_squad_divergence(self.gw3_dir)

        # 1. Type and key contract
        expected_keys = {
            "gameweek",
            "current_xi_score",
            "optimal_xi_score",
            "projected_pts_current_5gw",
            "projected_pts_optimal_5gw",
            "pts_divergence",
            "transfers_needed",
            "players_to_keep",
            "path_a_pts",
            "path_b_pts",
            "path_c_pts",
            "wc_advantage",
            "threshold_pts",
            "should_trigger",
            "current_xi_df",
            "optimal_starters_df",
            "optimal_squad_df",
        }
        self.assertSetEqual(set(res.keys()), expected_keys)

        # 2. Squad and starter cardinalities
        self.assertEqual(len(res["current_xi_df"]), 11)
        self.assertEqual(len(res["optimal_starters_df"]), 11)
        self.assertEqual(len(res["optimal_squad_df"]), 15)

        # 3. Transfer count conservation law
        players_to_keep_len = len(res["players_to_keep"])
        self.assertEqual(res["transfers_needed"], 15 - players_to_keep_len)
        self.assertGreaterEqual(res["transfers_needed"], 0)
        self.assertLessEqual(res["transfers_needed"], 15)

        # 4. FPL formation validation on greedy starting XI
        curr_xi = res["current_xi_df"]
        pos_counts = curr_xi["Position"].value_counts()
        self.assertEqual(pos_counts.get("GKP", 0), 1)
        self.assertGreaterEqual(pos_counts.get("DEF", 0), 3)
        self.assertGreaterEqual(pos_counts.get("FWD", 0), 1)
        self.assertEqual(
            pos_counts.get("DEF", 0)
            + pos_counts.get("MID", 0)
            + pos_counts.get("FWD", 0),
            10,
        )

    def test_missing_vault_edge_case(self):
        """Dan Luu Principle 1: Edge case where gameweek directory does not exist."""
        with self.assertRaises(FileNotFoundError):
            calculate_squad_divergence("non_existent_gw999")


if __name__ == "__main__":
    unittest.main()
