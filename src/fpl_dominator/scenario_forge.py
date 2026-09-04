"""Scenario Forge Matrix Builder and Parameter Generators.

Implements ScenarioDefinition and generators for multi-dimensional Cartesian exploration
(RFC-008) and single-axis parameter gradients (RFC-009) to map player survival curves.
"""

from dataclasses import dataclass
from typing import Sequence

from .temporal_decay import (
    generate_exponential_weights,
    generate_linear_weights,
    generate_scenario_signature,
    generate_step_weights,
    interpolate_gradient,
)


@dataclass(frozen=True)
class ScenarioDefinition:
    """Represents a single scenario parameterization in the Scenario Forge.

    Attributes:
        name: Compact unique scenario identifier / signature (e.g., 'EXP:0.75').
        model_type: Decay model archetype ('exponential', 'linear', 'step', 'flat').
        param_value: Numerical parameter value (decay_rate, slope, or cutoff).
        weights: List of fixture horizon weights W(t).
        form_factor_weight: Optional form weighting multiplier
            (None = use config default).
    """

    name: str
    model_type: str
    param_value: float
    weights: list[float]
    form_factor_weight: float | None = None

    def __post_init__(self) -> None:
        """Validates scenario integrity and mathematical invariants."""
        if not self.name or not self.name.strip():
            raise ValueError("Scenario name cannot be empty")
        if not self.model_type or not self.model_type.strip():
            raise ValueError("Scenario model_type cannot be empty")
        if not self.weights:
            raise ValueError("Scenario weights cannot be empty")
        for w in self.weights:
            if w < 0.0:
                raise ValueError(f"Scenario weight cannot be negative, got {w}")
        if self.form_factor_weight is not None and self.form_factor_weight < 0.0:
            raise ValueError(
                f"Form factor weight must be non-negative, got "
                f"{self.form_factor_weight}"
            )


def compute_scenario_weights(
    model_type: str, param_value: float, horizon: int = 5
) -> list[float]:
    """Computes fixture weights for a given decay model archetype and parameter.

    Args:
        model_type: Decay model ('exponential', 'linear', 'step', 'flat').
        param_value: Model parameter (decay_rate for exp, slope for lin,
            cutoff for step).
        horizon: Temporal fixture horizon length (default: 5).

    Returns:
        List of computed float weights for t = 0 .. horizon-1.

    Raises:
        ValueError: If model_type is unknown or parameters are invalid.
    """
    clean_model = model_type.strip().lower()
    if clean_model in ("exponential", "exp"):
        return generate_exponential_weights(decay_rate=param_value, horizon=horizon)
    if clean_model in ("linear", "lin"):
        return generate_linear_weights(slope=param_value, horizon=horizon)
    if clean_model in ("step", "horizon"):
        return generate_step_weights(cutoff=int(param_value), horizon=horizon)
    if clean_model in ("flat", "constant"):
        if horizon < 1:
            raise ValueError(f"Horizon must be >= 1, got {horizon}")
        return [1.0] * horizon

    raise ValueError(
        f"Unsupported decay model '{model_type}'. "
        f"Supported models: 'exponential', 'linear', 'step', 'flat'."
    )


def create_scenario(
    model_type: str,
    param_value: float,
    horizon: int = 5,
    form_factor_weight: float | None = None,
    name: str | None = None,
) -> ScenarioDefinition:
    """Factory helper to construct a validated ScenarioDefinition.

    If name is None, it is automatically derived via generate_scenario_signature.

    Args:
        model_type: Decay model ('exponential', 'linear', 'step', 'flat').
        param_value: Parameter value for the model.
        horizon: Temporal fixture horizon length (default: 5).
        form_factor_weight: Optional form factor weight modifier.
        name: Optional explicit scenario name.

    Returns:
        Validated ScenarioDefinition instance.
    """
    clean_model = model_type.strip().lower()
    weights = compute_scenario_weights(clean_model, param_value, horizon=horizon)
    scenario_name = name or generate_scenario_signature(
        clean_model, param_value, form_weight=form_factor_weight
    )
    return ScenarioDefinition(
        name=scenario_name,
        model_type=clean_model,
        param_value=param_value,
        weights=weights,
        form_factor_weight=form_factor_weight,
    )


def generate_cartesian_matrix(
    decay_rates: Sequence[float] = (0.4, 0.6, 0.8),
    form_factor_weights: Sequence[float | None] = (0.5, 0.7, 0.9),
    model_type: str | Sequence[str] = "exponential",
    horizon: int = 5,
    param_values: Sequence[float] | None = None,
) -> list[ScenarioDefinition]:
    """Generates Cartesian product scenarios across parameter dimensions.

    Explores multi-dimensional grid of (decay_rate x form_factor_weight)
    as specified in RFC-008.

    Args:
        decay_rates: Sequence of decay rates / parameter values to evaluate.
        form_factor_weights: Sequence of form factor multipliers (can include None).
        model_type: Model archetype string or sequence of archetype strings.
        horizon: Fixture horizon length (default: 5).
        param_values: Optional alias for decay_rates / parameter values.

    Returns:
        List of ScenarioDefinition instances covering all combinations.
    """
    models = [model_type] if isinstance(model_type, str) else list(model_type)
    values = list(param_values if param_values is not None else decay_rates)
    form_weights = list(form_factor_weights)

    scenarios: list[ScenarioDefinition] = []
    for m in models:
        for p in values:
            for fw in form_weights:
                scenarios.append(
                    create_scenario(
                        model_type=m,
                        param_value=float(p),
                        horizon=horizon,
                        form_factor_weight=fw,
                    )
                )
    return scenarios


def generate_gradient_matrix(
    model_type: str = "exponential",
    start: float = 1.0,
    end: float = 0.0,
    steps: int = 5,
    horizon: int = 5,
    form_factor_weight: float | None = None,
) -> list[ScenarioDefinition]:
    """Generates single-axis parameter gradient scenarios (RFC-009).

    Interpolates `steps` parameter values from `start` to `end` to map
    the selection survival curve.

    Args:
        model_type: Decay model archetype ('exponential', 'linear', 'step').
        start: Starting parameter extrema (e.g. 1.0 for Eternalist).
        end: Ending parameter extrema (e.g. 0.0 for Pure Sniper).
        steps: Total number of interpolated points (must be >= 2).
        horizon: Fixture horizon length (default: 5).
        form_factor_weight: Optional form factor weight modifier.

    Returns:
        List of ScenarioDefinition instances across the interpolated gradient.
    """
    clean_model = model_type.strip().lower()
    param_values = interpolate_gradient(start=start, end=end, steps=steps)

    return [
        create_scenario(
            model_type=clean_model,
            param_value=p,
            horizon=horizon,
            form_factor_weight=form_factor_weight,
        )
        for p in param_values
    ]


# Functional alias for parity with RFC documentation
generate_gradient_scenarios = generate_gradient_matrix

__all__ = [
    "ScenarioDefinition",
    "compute_scenario_weights",
    "create_scenario",
    "generate_cartesian_matrix",
    "generate_gradient_matrix",
    "generate_gradient_scenarios",
]
