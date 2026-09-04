"""Unit tests for Scenario Forge matrix builder and parameter generators.

Validates ScenarioDefinition invariants, Cartesian matrix products (RFC-008),
and single-axis parameter gradients (RFC-009).
"""

import unittest

from fpl_dominator.scenario_forge import (
    ScenarioDefinition,
    compute_scenario_weights,
    create_scenario,
    generate_cartesian_matrix,
    generate_gradient_matrix,
    generate_gradient_scenarios,
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


if __name__ == "__main__":
    unittest.main()
