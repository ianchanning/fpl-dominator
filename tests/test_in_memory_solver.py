"""Unit and anti-gambit smoke tests for in-memory Pyomo solver decoupling (Task 2.3).

Validates:
1. Anti-Gambit Smoke Test: 5 consecutive in-memory solves produce identical results
   without state leakage, cross-talk, or memory corruption.
2. Baseline Parity: In-memory solve matches expected squad and financial metrics.
3. Parametric Sensitivity & Recovery: Modifying hyperparameters (e.g., form_factor)
   alters the solution deterministically; restoring baseline recovers bit-for-bit.
4. Immutability: SquadSolution dataclass is frozen and defensive.
"""

import os
import unittest

import pandas as pd

from fpl_dominator.chimera_pyomo_v2 import (
    SquadSolution,
    forge_pyomo_squad,
    solve_chimera_squad,
)


class TestInMemorySolverDecoupling(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gw3_omniscient_path = "gw3/fpl_master_database_OMNISCIENT.csv"
        cls.set_pieces_path = "set_pieces.csv"
        if not os.path.exists(cls.gw3_omniscient_path):
            raise unittest.SkipTest(f"Missing test fixture: {cls.gw3_omniscient_path}")
        cls.omniscient_df = pd.read_csv(cls.gw3_omniscient_path)

    def test_five_consecutive_solves_anti_gambit(self):
        """Smoke test: 5 consecutive solves must yield bit-identical results."""
        solutions: list[SquadSolution] = []
        for i in range(5):
            sol = solve_chimera_squad(
                self.omniscient_df.copy(),
                set_pieces_path=self.set_pieces_path,
            )
            self.assertTrue(
                sol.success, f"Solve {i + 1} failed to find optimal solution"
            )
            solutions.append(sol)

        baseline = solutions[0]
        baseline_starters = sorted(baseline.starters["Surname"].tolist())
        baseline_bench = sorted(baseline.bench["Surname"].tolist())

        for idx, sol in enumerate(solutions[1:], start=2):
            starters = sorted(sol.starters["Surname"].tolist())
            bench = sorted(sol.bench["Surname"].tolist())

            self.assertEqual(
                starters,
                baseline_starters,
                f"Run {idx} starters diverged from baseline: {starters}",
            )
            self.assertEqual(
                bench,
                baseline_bench,
                f"Run {idx} bench diverged from baseline: {bench}",
            )
            self.assertAlmostEqual(
                sol.total_score,
                baseline.total_score,
                places=4,
                msg=(
                    f"Run {idx} score drift: {sol.total_score} != "
                    f"{baseline.total_score}"
                ),
            )
            self.assertAlmostEqual(
                sol.total_cost,
                baseline.total_cost,
                places=2,
                msg=f"Run {idx} cost drift: {sol.total_cost} != {baseline.total_cost}",
            )
            self.assertAlmostEqual(
                sol.bank,
                baseline.bank,
                places=2,
                msg=f"Run {idx} bank drift: {sol.bank} != {baseline.bank}",
            )

    def test_parametric_isolation_and_recovery(self):
        """Verify solver state isolation when hyperparameters change and recover."""
        config_base = {"form_factor_weight": 0.7}
        sol_base1 = solve_chimera_squad(
            self.omniscient_df.copy(),
            set_pieces_path=self.set_pieces_path,
            solver_config=config_base,
        )

        config_perturbed = {"form_factor_weight": 0.0}
        sol_perturbed = solve_chimera_squad(
            self.omniscient_df.copy(),
            set_pieces_path=self.set_pieces_path,
            solver_config=config_perturbed,
        )

        sol_base2 = solve_chimera_squad(
            self.omniscient_df.copy(),
            set_pieces_path=self.set_pieces_path,
            solver_config=config_base,
        )

        self.assertEqual(
            sorted(sol_base1.starters["Surname"].tolist()),
            sorted(sol_base2.starters["Surname"].tolist()),
        )
        self.assertEqual(sol_base1.total_score, sol_base2.total_score)
        self.assertNotEqual(sol_base1.total_score, sol_perturbed.total_score)

    def test_squad_solution_immutability(self):
        """Verify SquadSolution dataclass is frozen and defensive."""
        sol = solve_chimera_squad(
            self.omniscient_df.copy(),
            set_pieces_path=self.set_pieces_path,
        )
        self.assertIsInstance(sol, SquadSolution)
        with self.assertRaises(Exception):
            sol.total_score = 999.9  # type: ignore

    def test_disk_baseline_parity(self):
        """Verify in-memory solve matches forge_pyomo_squad disk harness baseline."""
        success, disk_starters, disk_bench = forge_pyomo_squad("gw3", return_squad=True)
        self.assertTrue(success)

        in_mem_sol = solve_chimera_squad(
            self.omniscient_df.copy(),
            set_pieces_path=self.set_pieces_path,
        )
        self.assertTrue(in_mem_sol.success)

        self.assertEqual(
            sorted(disk_starters["Surname"].tolist()),
            sorted(in_mem_sol.starters["Surname"].tolist()),
        )
        self.assertEqual(
            sorted(disk_bench["Surname"].tolist()),
            sorted(in_mem_sol.bench["Surname"].tolist()),
        )
        self.assertAlmostEqual(
            float(disk_starters["Final_Score"].sum()),
            in_mem_sol.total_score,
            places=2,
        )

    def test_dan_luu_independent_fpl_rules_oracle(self):
        """Dan Luu Principle 2: Independent verification oracle for FPL & MILP rules."""
        sol = solve_chimera_squad(
            self.omniscient_df.copy(),
            set_pieces_path=self.set_pieces_path,
        )
        self.assertTrue(sol.success)
        violations = _independently_verify_fpl_rules(sol, max_budget=100.0)
        self.assertEqual(
            violations, [], f"Oracle detected rule violations: {violations}"
        )

    def test_squad_solution_domain_properties(self):
        """Dan Luu Principle 3: Verify rich domain details from SquadSolution."""
        sol = solve_chimera_squad(
            self.omniscient_df.copy(),
            set_pieces_path=self.set_pieces_path,
        )
        self.assertTrue(sol.success)

        # 1. Formation format check (e.g., '3-5-2', '4-4-2')
        self.assertRegex(sol.formation, r"^[3-5]-[2-5]-[1-3]$")
        d, m, f = map(int, sol.formation.split("-"))
        self.assertEqual(d + m + f, 10, "Outfield starting players must equal 10")

        # 2. Captain and Vice-Captain identification
        self.assertIsNotNone(sol.captain)
        self.assertIsNotNone(sol.vice_captain)
        self.assertIn(sol.captain, sol.starters["Surname"].tolist())
        self.assertIn(sol.vice_captain, sol.starters["Surname"].tolist())
        self.assertNotEqual(sol.captain, sol.vice_captain)

        # Confirm captain has strictly maximum Final_Score
        max_score = sol.starters["Final_Score"].max()
        captain_row = sol.starters[sol.starters["Surname"] == sol.captain].iloc[0]
        self.assertEqual(captain_row["Final_Score"], max_score)

        # 3. Positional costs accounting
        costs = sol.position_costs
        self.assertSetEqual(set(costs.keys()), {"GKP", "DEF", "MID", "FWD"})
        self.assertAlmostEqual(sum(costs.values()), sol.total_cost, places=1)

        # 4. Red zone starters audit
        self.assertLessEqual(len(sol.red_zone_starters), 5)

    def test_infeasible_budget_boundary_edge_case(self):
        """Dan Luu Principle 1: Edge case where budget constraint is impossible."""
        # Scale all prices so minimum possible squad costs > 100.0 (50.0/player)
        astronomical_df = self.omniscient_df.copy()
        astronomical_df["Price"] = 50.0

        sol = solve_chimera_squad(
            astronomical_df,
            set_pieces_path=self.set_pieces_path,
        )
        # Solver must cleanly report failure, not crash or raise unhandled exceptions
        self.assertFalse(sol.success)
        self.assertTrue(sol.starters.empty)
        self.assertTrue(sol.bench.empty)
        self.assertTrue(sol.squad.empty)
        self.assertEqual(sol.formation, "0-0-0")
        self.assertIsNone(sol.captain)

    def test_empty_and_undersized_dataframe_guard(self):
        """Dan Luu Principle 1: Edge case with empty/undersized pool (< 15 players)."""
        empty_sol = solve_chimera_squad(
            pd.DataFrame(),
            set_pieces_path=self.set_pieces_path,
        )
        self.assertFalse(empty_sol.success)
        self.assertEqual(empty_sol.formation, "0-0-0")

        undersized_sol = solve_chimera_squad(
            self.omniscient_df.iloc[:10].copy(),
            set_pieces_path=self.set_pieces_path,
        )
        self.assertFalse(undersized_sol.success)
        self.assertEqual(undersized_sol.formation, "0-0-0")

    def test_defensive_hyperparameter_type_coercion(self):
        """Dan Luu Principle 1: Defensive extractors coerce string inputs safely."""
        config_strings = {
            "thrift_factor": "0.002",
            "bench_potency_epsilon": "0.00005",
            "form_factor_weight": "0.85",
            "red_zone_threshold": "1300.0",
            "red_zone_limit": "4",
        }
        sol = solve_chimera_squad(
            self.omniscient_df.copy(),
            set_pieces_path=self.set_pieces_path,
            solver_config=config_strings,
        )
        self.assertTrue(sol.success)
        violations = _independently_verify_fpl_rules(
            sol, max_budget=100.0, red_zone_threshold=1300.0, red_zone_limit=4
        )
        self.assertEqual(violations, [])

    def test_unrecognized_form_model_fallback(self):
        """Dan Luu Principle 1: Unrecognized form_model falls back to Form_Factor."""
        config_unknown = {"form_model": "quantum_unrecognized_model"}
        sol = solve_chimera_squad(
            self.omniscient_df.copy(),
            set_pieces_path=self.set_pieces_path,
            solver_config=config_unknown,
        )
        self.assertTrue(sol.success)
        self.assertEqual(_independently_verify_fpl_rules(sol), [])

    def test_forge_pyomo_squad_overload_contracts(self):
        """Dan Luu Principle 3: Verify @overload contracts for forge_pyomo_squad."""
        # Overload 1: return_squad=False (or default) returns strictly bool
        res_bool = forge_pyomo_squad("gw3", return_squad=False)
        self.assertIsInstance(res_bool, bool)
        self.assertTrue(res_bool)

        # Overload 2: return_squad=True returns strictly 3-element tuple
        res_tuple = forge_pyomo_squad("gw3", return_squad=True)
        self.assertIsInstance(res_tuple, tuple)
        self.assertEqual(len(res_tuple), 3)
        success_flag, starters_df, bench_df = res_tuple
        self.assertIsInstance(success_flag, bool)
        self.assertIsInstance(starters_df, pd.DataFrame)
        self.assertIsInstance(bench_df, pd.DataFrame)
        self.assertEqual(len(starters_df), 11)
        self.assertEqual(len(bench_df), 4)


def _independently_verify_fpl_rules(
    solution: SquadSolution,
    max_budget: float = 100.0,
    red_zone_threshold: float = 1250.0,
    red_zone_limit: int = 5,
) -> list[str]:
    """Dan Luu Independent Verification Oracle.

    Re-verifies all FPL combinatorial rules and Chimera invariants independently
    from first principles without relying on Pyomo constraint evaluations.
    """
    violations: list[str] = []

    if not solution.success:
        violations.append("Solution marked as unsuccessful.")
        return violations

    squad = solution.squad
    starters = solution.starters
    bench = solution.bench

    # 1. Cardinalities
    if len(squad) != 15:
        violations.append(f"Squad size violation: expected 15, got {len(squad)}")
    if len(starters) != 11:
        violations.append(f"Starter size violation: expected 11, got {len(starters)}")
    if len(bench) != 4:
        violations.append(f"Bench size violation: expected 4, got {len(bench)}")

    # 2. Subset & Disjointness
    starter_names = set(starters["Surname"])
    bench_names = set(bench["Surname"])
    squad_names = set(squad["Surname"])

    if not starter_names.issubset(squad_names):
        violations.append("Starters are not a strict subset of squad.")
    if not bench_names.issubset(squad_names):
        violations.append("Bench is not a strict subset of squad.")
    if not starter_names.isdisjoint(bench_names):
        violations.append(f"Starters and bench overlap: {starter_names & bench_names}")

    # 3. Positional Squad Quotas
    squad_pos = squad["Position"].value_counts()
    if squad_pos.get("GKP", 0) != 2:
        violations.append(
            f"GKP squad quota violation: expected 2, got {squad_pos.get('GKP', 0)}"
        )
    if squad_pos.get("DEF", 0) != 5:
        violations.append(
            f"DEF squad quota violation: expected 5, got {squad_pos.get('DEF', 0)}"
        )
    if squad_pos.get("MID", 0) != 5:
        violations.append(
            f"MID squad quota violation: expected 5, got {squad_pos.get('MID', 0)}"
        )
    if squad_pos.get("FWD", 0) != 3:
        violations.append(
            f"FWD squad quota violation: expected 3, got {squad_pos.get('FWD', 0)}"
        )

    # 4. Positional Starter Quotas
    starter_pos = starters["Position"].value_counts()
    gkp_s = starter_pos.get("GKP", 0)
    def_s = starter_pos.get("DEF", 0)
    mid_s = starter_pos.get("MID", 0)
    fwd_s = starter_pos.get("FWD", 0)

    if gkp_s != 1:
        violations.append(f"Starting GKP quota violation: expected 1, got {gkp_s}")
    if def_s < 3:
        violations.append(f"Starting DEF minimum violation: expected >= 3, got {def_s}")
    if fwd_s < 1:
        violations.append(f"Starting FWD minimum violation: expected >= 1, got {fwd_s}")
    if def_s + mid_s + fwd_s != 10:
        violations.append(
            f"Outfield starters sum violation: expected 10, got {def_s + mid_s + fwd_s}"
        )

    # 5. Club Quota (Max 3 per team)
    team_counts = squad["Team_TLA"].value_counts()
    for team, count in team_counts.items():
        if count > 3:
            violations.append(f"Team limit exceeded for {team}: {count} > 3")

    # 6. Budget & Financial Conservation
    raw_cost = round(float(squad["Price"].sum()), 1)
    if raw_cost > max_budget:
        violations.append(f"Budget exceeded: {raw_cost} > {max_budget}")
    if round(solution.total_cost, 1) != raw_cost:
        violations.append(
            f"Cost discrepancy: total_cost={solution.total_cost} "
            f"!= squad price sum={raw_cost}"
        )
    if round(solution.total_cost + solution.bank, 1) != max_budget:
        violations.append(
            f"Financial conservation violated: cost ({solution.total_cost}) "
            f"+ bank ({solution.bank}) != {max_budget}"
        )

    # 7. Red Zone Quota
    if "Effective_FDR_Horizon_5GW" in starters.columns:
        rz_starters = starters[
            starters["Effective_FDR_Horizon_5GW"] > red_zone_threshold
        ]
        if len(rz_starters) > red_zone_limit:
            violations.append(
                f"Red zone limit exceeded: {len(rz_starters)} > {red_zone_limit}"
            )

    return violations


if __name__ == "__main__":
    unittest.main()
