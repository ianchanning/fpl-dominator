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


if __name__ == "__main__":
    unittest.main()
