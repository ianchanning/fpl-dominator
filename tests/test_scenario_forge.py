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
    format_dataframe_to_markdown,
    generate_cartesian_matrix,
    generate_gradient_matrix,
    generate_gradient_scenarios,
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


if __name__ == "__main__":
    unittest.main()
