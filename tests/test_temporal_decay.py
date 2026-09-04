"""Unit tests for functional temporal decay weight generators and gradients.

Validates mathematical invariants, boundary conditions, and signature formatting
from RFC-008 and RFC-009.
"""

import unittest

from fpl_dominator.temporal_decay import (
    generate_exponential_weights,
    generate_linear_weights,
    generate_scenario_signature,
    generate_step_weights,
    interpolate_gradient,
)


class TestTemporalDecay(unittest.TestCase):
    def test_linear_weights_standard(self):
        weights = generate_linear_weights(slope=0.2, horizon=5)
        self.assertEqual(weights, [1.0, 0.8, 0.6, 0.4, 0.2])

    def test_linear_weights_clamping(self):
        weights = generate_linear_weights(slope=0.5, horizon=5)
        self.assertEqual(weights, [1.0, 0.5, 0.0, 0.0, 0.0])

    def test_linear_weights_validation(self):
        with self.assertRaises(ValueError):
            generate_linear_weights(slope=-0.1)
        with self.assertRaises(ValueError):
            generate_linear_weights(slope=0.2, horizon=0)

    def test_exponential_weights_standard(self):
        weights = generate_exponential_weights(decay_rate=0.5, horizon=5)
        self.assertEqual(weights, [1.0, 0.5, 0.25, 0.125, 0.0625])

    def test_exponential_weights_extrema(self):
        # Pure Sniper (decay_rate = 0.0) -> only GW0 has weight 1.0
        sniper = generate_exponential_weights(decay_rate=0.0, horizon=5)
        self.assertEqual(sniper, [1.0, 0.0, 0.0, 0.0, 0.0])

        # Eternalist (decay_rate = 1.0) -> all GWs have weight 1.0
        eternalist = generate_exponential_weights(decay_rate=1.0, horizon=5)
        self.assertEqual(eternalist, [1.0, 1.0, 1.0, 1.0, 1.0])

    def test_exponential_weights_validation(self):
        with self.assertRaises(ValueError):
            generate_exponential_weights(decay_rate=-0.5)
        with self.assertRaises(ValueError):
            generate_exponential_weights(decay_rate=0.5, horizon=-1)

    def test_step_weights_standard(self):
        weights = generate_step_weights(cutoff=3, horizon=5)
        self.assertEqual(weights, [1.0, 1.0, 1.0, 0.0, 0.0])

    def test_step_weights_extrema(self):
        all_zeros = generate_step_weights(cutoff=0, horizon=5)
        self.assertEqual(all_zeros, [0.0, 0.0, 0.0, 0.0, 0.0])

        all_ones = generate_step_weights(cutoff=10, horizon=5)
        self.assertEqual(all_ones, [1.0, 1.0, 1.0, 1.0, 1.0])

    def test_interpolate_gradient(self):
        grad_descending = interpolate_gradient(start=1.0, end=0.0, steps=5)
        self.assertEqual(grad_descending, [1.0, 0.75, 0.5, 0.25, 0.0])

        grad_ascending = interpolate_gradient(start=0.1, end=0.5, steps=5)
        self.assertEqual(grad_ascending, [0.1, 0.2, 0.3, 0.4, 0.5])

        with self.assertRaises(ValueError):
            interpolate_gradient(start=1.0, end=0.0, steps=1)

    def test_scenario_signatures(self):
        self.assertEqual(generate_scenario_signature("exponential", 0.75), "EXP:0.75")
        self.assertEqual(generate_scenario_signature("linear", 0.2), "LIN:0.20")
        self.assertEqual(generate_scenario_signature("step", 3), "STEP:3")
        self.assertEqual(
            generate_scenario_signature("exponential", 0.6, form_weight=0.7),
            "EXP:0.60_FW:0.7",
        )


if __name__ == "__main__":
    unittest.main()
