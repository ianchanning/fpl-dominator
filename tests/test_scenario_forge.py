"""Unit tests for Scenario Forge matrix builder and parameter generators.

Validates ScenarioDefinition invariants, Cartesian matrix products (RFC-008),
and single-axis parameter gradients (RFC-009).
"""

import os
import unittest

import pandas as pd

from fpl_dominator.scenario_forge import (
    PlayerScenarioStats,
    ScenarioDefinition,
    ScenarioRunReport,
    classify_survival_curve,
    compute_scenario_weights,
    create_scenario,
    filter_static_bench_players,
    format_ascii_matrix,
    format_dataframe_to_markdown,
    format_weight_registry,
    generate_cartesian_matrix,
    generate_gradient_matrix,
    generate_gradient_scenarios,
    highlight_starting_alterations,
    run_scenario_matrix,
)


class TestScenarioForge(unittest.TestCase):
    def test_scenario_definition_instantiation_and_immutability(self):
        scenario = ScenarioDefinition(
            name="EXP:0.75",
            model_type="exponential",
            param_value=0.75,
            weights=[1.0, 0.75, 0.5625, 0.421875, 0.316406],
            form_factor_weight=0.7,
        )
        self.assertEqual(scenario.name, "EXP:0.75")
        self.assertEqual(scenario.model_type, "exponential")
        self.assertEqual(scenario.param_value, 0.75)
        self.assertEqual(len(scenario.weights), 5)
        self.assertEqual(scenario.form_factor_weight, 0.7)

        # Frozen dataclass immutability check
        with self.assertRaises(Exception):
            scenario.param_value = 0.50  # type: ignore

    def test_scenario_definition_validation(self):
        # Empty name
        with self.assertRaises(ValueError):
            ScenarioDefinition(
                name="",
                model_type="exponential",
                param_value=0.5,
                weights=[1.0, 0.5],
            )

        # Empty model type
        with self.assertRaises(ValueError):
            ScenarioDefinition(
                name="TEST",
                model_type="",
                param_value=0.5,
                weights=[1.0, 0.5],
            )

        # Empty weights
        with self.assertRaises(ValueError):
            ScenarioDefinition(
                name="TEST",
                model_type="exponential",
                param_value=0.5,
                weights=[],
            )

        # Negative weight
        with self.assertRaises(ValueError):
            ScenarioDefinition(
                name="TEST",
                model_type="exponential",
                param_value=0.5,
                weights=[1.0, -0.2],
            )

        # Negative form_factor_weight
        with self.assertRaises(ValueError):
            ScenarioDefinition(
                name="TEST",
                model_type="exponential",
                param_value=0.5,
                weights=[1.0, 0.5],
                form_factor_weight=-0.1,
            )

    def test_compute_scenario_weights(self):
        exp_w = compute_scenario_weights("exponential", 0.5, horizon=5)
        self.assertEqual(exp_w, [1.0, 0.5, 0.25, 0.125, 0.0625])

        lin_w = compute_scenario_weights("linear", 0.2, horizon=5)
        self.assertEqual(lin_w, [1.0, 0.8, 0.6, 0.4, 0.2])

        step_w = compute_scenario_weights("step", 3, horizon=5)
        self.assertEqual(step_w, [1.0, 1.0, 1.0, 0.0, 0.0])

        flat_w = compute_scenario_weights("flat", 0.0, horizon=5)
        self.assertEqual(flat_w, [1.0, 1.0, 1.0, 1.0, 1.0])

        with self.assertRaises(ValueError):
            compute_scenario_weights("unknown_model", 0.5)

    def test_create_scenario(self):
        scenario = create_scenario(
            model_type="exponential",
            param_value=0.6,
            horizon=5,
            form_factor_weight=0.7,
        )
        self.assertEqual(scenario.name, "EXP:0.60_FW:0.7")
        self.assertEqual(scenario.weights[0], 1.0)
        self.assertEqual(scenario.weights[1], 0.6)
        self.assertEqual(scenario.form_factor_weight, 0.7)

        # Custom name override
        custom_scenario = create_scenario(
            model_type="linear",
            param_value=0.2,
            name="CUSTOM_LIN",
        )
        self.assertEqual(custom_scenario.name, "CUSTOM_LIN")

    def test_generate_cartesian_matrix(self):
        # 3 decay rates x 3 form weights = 9 scenarios
        scenarios = generate_cartesian_matrix(
            decay_rates=[0.4, 0.6, 0.8],
            form_factor_weights=[0.5, 0.7, 0.9],
            model_type="exponential",
            horizon=5,
        )
        self.assertEqual(len(scenarios), 9)

        signatures = [s.name for s in scenarios]
        self.assertIn("EXP:0.40_FW:0.5", signatures)
        self.assertIn("EXP:0.60_FW:0.7", signatures)
        self.assertIn("EXP:0.80_FW:0.9", signatures)

        # Test param_values alias and multi-model support
        multi_model_scenarios = generate_cartesian_matrix(
            param_values=[0.5],
            form_factor_weights=[0.7],
            model_type=["exponential", "linear"],
        )
        self.assertEqual(len(multi_model_scenarios), 2)
        self.assertEqual(multi_model_scenarios[0].model_type, "exponential")
        self.assertEqual(multi_model_scenarios[1].model_type, "linear")

    def test_generate_gradient_matrix_exponential(self):
        scenarios = generate_gradient_matrix(
            model_type="exponential",
            start=1.0,
            end=0.0,
            steps=5,
            horizon=5,
        )
        self.assertEqual(len(scenarios), 5)
        self.assertEqual(scenarios[0].name, "EXP:1.00")
        self.assertEqual(scenarios[0].weights, [1.0, 1.0, 1.0, 1.0, 1.0])
        self.assertEqual(scenarios[2].name, "EXP:0.50")
        self.assertEqual(scenarios[2].weights, [1.0, 0.5, 0.25, 0.125, 0.0625])
        self.assertEqual(scenarios[4].name, "EXP:0.00")
        self.assertEqual(scenarios[4].weights, [1.0, 0.0, 0.0, 0.0, 0.0])

    def test_generate_gradient_matrix_linear_and_step(self):
        lin_scenarios = generate_gradient_scenarios(
            model_type="linear",
            start=0.1,
            end=0.5,
            steps=5,
            horizon=5,
        )
        self.assertEqual(len(lin_scenarios), 5)
        self.assertEqual(lin_scenarios[0].name, "LIN:0.10")
        self.assertEqual(lin_scenarios[4].name, "LIN:0.50")

        step_scenarios = generate_gradient_matrix(
            model_type="step",
            start=5.0,
            end=1.0,
            steps=5,
            horizon=5,
        )
        self.assertEqual(len(step_scenarios), 5)
        self.assertEqual(step_scenarios[0].name, "STEP:5")
        self.assertEqual(step_scenarios[0].weights, [1.0, 1.0, 1.0, 1.0, 1.0])
        self.assertEqual(step_scenarios[4].name, "STEP:1")
        self.assertEqual(step_scenarios[4].weights, [1.0, 0.0, 0.0, 0.0, 0.0])

    def test_classify_survival_curve(self):
        s_deep = create_scenario("flat", 1.0)  # sum = 5.0
        s_mid = create_scenario("exponential", 0.6)  # sum = 2.31
        s_shallow = create_scenario("exponential", 0.2)  # sum = 1.25
        all_sc = [s_deep, s_mid, s_shallow]

        # Immortal: selected in all scenarios
        cls_imm, rob_imm = classify_survival_curve(
            {s_deep.name, s_mid.name, s_shallow.name}, all_sc
        )
        self.assertEqual(cls_imm, "IMMORTAL")
        self.assertEqual(rob_imm, 1.0)

        # Horizon-Dependent: selected in deepest, not shallowest
        cls_hor, rob_hor = classify_survival_curve({s_deep.name, s_mid.name}, all_sc)
        self.assertEqual(cls_hor, "HORIZON-DEPENDENT")
        self.assertAlmostEqual(rob_hor, 0.6667, places=3)

        # Pure Punt: selected in shallowest, not deepest
        cls_punt, rob_punt = classify_survival_curve({s_shallow.name}, all_sc)
        self.assertEqual(cls_punt, "PURE PUNT")
        self.assertAlmostEqual(rob_punt, 0.3333, places=3)

        # Fringe: selected in deepest and shallowest (skipping middle)
        cls_fringe, rob_fringe = classify_survival_curve(
            {s_deep.name, s_shallow.name}, all_sc
        )
        self.assertEqual(cls_fringe, "FRINGE")
        self.assertAlmostEqual(rob_fringe, 0.6667, places=3)

        # Unselected
        cls_none, rob_none = classify_survival_curve(set(), all_sc)
        self.assertEqual(cls_none, "UNSELECTED")
        self.assertEqual(rob_none, 0.0)

    def test_format_dataframe_to_markdown(self):
        df = pd.DataFrame(
            [
                {"Surname": "Haaland", "Position": "FWD", "Robustness": "100%"},
                {"Surname": "Saka", "Position": "MID", "Robustness": "100%"},
            ]
        )
        md = format_dataframe_to_markdown(df)
        self.assertIn("| Surname | Position | Robustness |", md)
        self.assertIn("| Haaland | FWD | 100% |", md)

        empty_md = format_dataframe_to_markdown(pd.DataFrame())
        self.assertEqual(empty_md, "*Empty Matrix*")

    def test_run_scenario_matrix_validation(self):
        with self.assertRaises(ValueError):
            run_scenario_matrix("gw3", scenarios=[])

        with self.assertRaises(FileNotFoundError):
            sc = [create_scenario("flat", 1.0)]
            run_scenario_matrix("nonexistent_gw_vault", scenarios=sc)

    def test_run_scenario_matrix_gw3_smoke(self):
        if not os.path.exists("gw3/fpl_master_database_prophetic.csv"):
            raise unittest.SkipTest("Missing gw3 test fixtures")

        scenarios = [
            create_scenario("flat", 1.0),
            create_scenario("exponential", 0.6),
            create_scenario("exponential", 0.2),
        ]
        os.makedirs("temp/test_forge", exist_ok=True)
        report_md_path = "temp/test_forge/report_smoke.md"

        report = run_scenario_matrix(
            gameweek_dir="gw3",
            scenarios=scenarios,
            output_path=report_md_path,
        )

        self.assertIsInstance(report, ScenarioRunReport)
        self.assertEqual(report.total_solves, 3)
        self.assertEqual(report.successful_solves, 3)
        self.assertTrue(len(report.immortals) > 0)
        self.assertIsInstance(report.player_stats[0], PlayerScenarioStats)

        # Validate DataFrame generation
        df = report.to_dataframe()
        self.assertFalse(df.empty)
        self.assertIn("Surname", df.columns)
        self.assertIn("Position", df.columns)
        self.assertIn("Robustness", df.columns)
        self.assertIn("Classification", df.columns)

        # Validate Markdown output
        md_text = report.to_markdown()
        self.assertIn("# Scenario Forge Analysis: GW3", md_text)
        self.assertIn("--- WEIGHT REGISTRY (SOURCE OF TRUTH) ---", md_text)
        self.assertTrue(os.path.exists(report_md_path))

        # Cleanup test artifact
        if os.path.exists(report_md_path):
            os.remove(report_md_path)

    def test_filter_static_bench_players(self):
        static_bench = PlayerScenarioStats(
            surname="Dovin",
            position="GKP",
            team="COV",
            price=4.0,
            starter_appearances=0,
            bench_appearances=3,
            total_appearances=3,
            robustness_score=0.0,
            classification="UNSELECTED",
            scenario_selections={"S1": "[b]", "S2": "[b]", "S3": "[b]"},
        )
        immortal_starter = PlayerScenarioStats(
            surname="Haaland",
            position="FWD",
            team="MCI",
            price=15.5,
            starter_appearances=3,
            bench_appearances=0,
            total_appearances=3,
            robustness_score=1.0,
            classification="IMMORTAL",
            scenario_selections={"S1": "[X]", "S2": "[X]", "S3": "[X]"},
        )
        divergent_starter = PlayerScenarioStats(
            surname="Tarkowski",
            position="DEF",
            team="EVE",
            price=6.0,
            starter_appearances=2,
            bench_appearances=1,
            total_appearances=3,
            robustness_score=0.67,
            classification="HORIZON-DEPENDENT",
            scenario_selections={"S1": "[X]", "S2": "[X]", "S3": "[b]"},
        )

        self.assertTrue(static_bench.is_static_bench)
        self.assertFalse(immortal_starter.is_static_bench)
        self.assertFalse(divergent_starter.is_static_bench)

        self.assertFalse(static_bench.is_divergent_starter)
        self.assertFalse(immortal_starter.is_divergent_starter)
        self.assertTrue(divergent_starter.is_divergent_starter)

        filtered = filter_static_bench_players(
            [static_bench, immortal_starter, divergent_starter]
        )
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0].surname, "Haaland")
        self.assertEqual(filtered[1].surname, "Tarkowski")

    def test_highlight_starting_alterations(self):
        # Immortal: R=1.0 -> no divergence marker
        imm_selections = {"S1": "[X]", "S2": "[X]"}
        self.assertEqual(
            highlight_starting_alterations(imm_selections, robustness_score=1.0),
            {"S1": "[X]", "S2": "[X]"},
        )

        # Divergent starter: R=0.5 -> [X] marked as [X]*
        div_selections = {"S1": "[X]", "S2": "[b]", "S3": "."}
        highlighted = highlight_starting_alterations(
            div_selections, robustness_score=0.5, divergence_marker="*"
        )
        self.assertEqual(
            highlighted,
            {"S1": "[X]*", "S2": "[b]", "S3": "."},
        )

    def test_diff_first_noise_suppression_and_cues(self):
        if not os.path.exists("gw3/fpl_master_database_prophetic.csv"):
            raise unittest.SkipTest("Missing gw3 test fixtures")

        # 1. Test static bench suppression with near-identical scenarios
        scenarios_static = [
            create_scenario("flat", 1.0),
            create_scenario("exponential", 0.99),
        ]
        report_static = run_scenario_matrix("gw3", scenarios=scenarios_static)
        self.assertTrue(len(report_static.static_bench_players) > 0)

        full_df = report_static.to_dataframe(suppress_static_bench=False)
        diff_df = report_static.to_dataframe(
            suppress_static_bench=True, highlight_divergence=True
        )
        self.assertGreater(len(full_df), len(diff_df))
        for bench_surname in report_static.static_bench_players:
            self.assertNotIn(bench_surname, diff_df["Surname"].tolist())

        # Test suppress_all_bench isolates starting XI players (11 starters)
        starter_only_df = report_static.to_dataframe(suppress_all_bench=True)
        self.assertEqual(len(starter_only_df), 11)

        # 2. Test starting alterations with divergent scenarios
        scenarios_divergent = [
            create_scenario("flat", 1.0),
            create_scenario("exponential", 0.2),
        ]
        report_div = run_scenario_matrix("gw3", scenarios=scenarios_divergent)
        diff_div_df = report_div.to_dataframe(
            suppress_static_bench=True, highlight_divergence=True
        )
        for div_surname in report_div.divergent_starters:
            div_row = diff_div_df[diff_div_df["Surname"] == div_surname]
            if not div_row.empty:
                has_cue = any(
                    "[X]*" in str(div_row.iloc[0][sc.name])
                    for sc in scenarios_divergent
                )
                self.assertTrue(has_cue)

        # Markdown includes Diff-First and Legend notes
        md_text = report_static.to_markdown(
            suppress_static_bench=True, highlight_divergence=True
        )
        self.assertIn("*Diff-First Noise Suppression:*", md_text)
        self.assertIn("*Legend:*", md_text)

    def test_format_weight_registry(self):
        scenarios = [
            create_scenario("exponential", 1.0),
            create_scenario("exponential", 0.75),
            create_scenario("exponential", 0.5),
            create_scenario("exponential", 0.25),
            create_scenario("exponential", 0.0),
        ]
        registry_text = format_weight_registry(scenarios)
        self.assertIn("--- WEIGHT REGISTRY (SOURCE OF TRUTH) ---", registry_text)
        self.assertIn("EXP:1.00  -> [1.00, 1.00, 1.00, 1.00, 1.00]", registry_text)
        self.assertIn("EXP:0.50  -> [1.00, 0.50, 0.25, 0.12, 0.06]", registry_text)
        self.assertIn("EXP:0.00  -> [1.00, 0.00, 0.00, 0.00, 0.00]", registry_text)

    def test_format_ascii_matrix(self):
        df = pd.DataFrame(
            [
                {
                    "Pos": "FWD",
                    "Surname": "Haaland",
                    "EXP:1.00": "[X]",
                    "EXP:0.50": "[X]",
                    "Robust": "100%",
                },
                {
                    "Pos": "MID",
                    "Surname": "Saka",
                    "EXP:1.00": "[X]",
                    "EXP:0.50": "[X]",
                    "Robust": "100%",
                },
            ]
        )
        table_ascii = format_ascii_matrix(df)
        self.assertIn("Haaland", table_ascii)
        self.assertIn("Saka", table_ascii)
        self.assertIn("-----", table_ascii)

        empty_ascii = format_ascii_matrix(pd.DataFrame())
        self.assertEqual(empty_ascii, "No players to display.")

    def test_report_to_terminal_and_write_markdown(self):
        if not os.path.exists("gw3/fpl_master_database_prophetic.csv"):
            raise unittest.SkipTest("Missing gw3 test fixtures")

        scenarios = [
            create_scenario("flat", 1.0),
            create_scenario("exponential", 0.6),
            create_scenario("exponential", 0.2),
        ]
        report = run_scenario_matrix("gw3", scenarios=scenarios)

        terminal_out = report.to_terminal(
            suppress_static_bench=True, highlight_divergence=True
        )
        self.assertIn("=== SCENARIO FORGE STABILITY MATRIX (GW3) ===", terminal_out)
        self.assertIn("[*] THE IMMORTALS", terminal_out)
        self.assertIn("--- WEIGHT REGISTRY (SOURCE OF TRUTH) ---", terminal_out)

        # Test writing report to gw3/scenario_forge.md
        written_path = report.write_markdown_report()
        self.assertEqual(written_path, "gw3/scenario_forge.md")
        self.assertTrue(os.path.exists("gw3/scenario_forge.md"))

        with open("gw3/scenario_forge.md", "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("# Scenario Forge Analysis: GW3", content)
        self.assertIn("--- WEIGHT REGISTRY (SOURCE OF TRUTH) ---", content)


if __name__ == "__main__":
    unittest.main()
