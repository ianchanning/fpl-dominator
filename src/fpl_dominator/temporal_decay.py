"""Functional temporal decay weight generators for FPL fixture horizons.

Provides pure mathematical weighting functions (Linear, Exponential, Step)
to parameterize fixture difficulty discounting without relying on static arrays.
"""

from typing import List


def generate_linear_weights(slope: float, horizon: int = 5) -> List[float]:
    """Generates linearly decaying weights: W(t) = max(0.0, 1.0 - t * slope).

    Args:
        slope: Rate of linear decay per gameweek step (>= 0.0).
        horizon: Number of fixture weeks in the temporal window (>= 1).

    Returns:
        List of float weights for t = 0 .. horizon-1.

    Raises:
        ValueError: If horizon < 1 or slope < 0.0.
    """
    if horizon < 1:
        raise ValueError(f"Horizon must be >= 1, got {horizon}")
    if slope < 0.0:
        raise ValueError(f"Slope must be >= 0.0, got {slope}")

    return [round(max(0.0, 1.0 - t * slope), 6) for t in range(horizon)]


def generate_exponential_weights(decay_rate: float, horizon: int = 5) -> List[float]:
    """Generates exponentially decaying weights: W(t) = decay_rate^t.

    Args:
        decay_rate: Multiplicative factor per step (0.0 <= decay_rate <= 1.0).
        horizon: Number of fixture weeks in the temporal window (>= 1).

    Returns:
        List of float weights for t = 0 .. horizon-1.

    Raises:
        ValueError: If horizon < 1 or decay_rate < 0.0.
    """
    if horizon < 1:
        raise ValueError(f"Horizon must be >= 1, got {horizon}")
    if decay_rate < 0.0:
        raise ValueError(f"Decay rate must be >= 0.0, got {decay_rate}")

    # For t=0, 0.0^0 = 1.0 (immediate fixture always has weight 1.0)
    weights: List[float] = []
    for t in range(horizon):
        if t == 0:
            weights.append(1.0)
        else:
            weights.append(round(decay_rate**t, 6))
    return weights


def generate_step_weights(cutoff: int, horizon: int = 5) -> List[float]:
    """Generates step-function weights: W(t) = 1.0 if t < cutoff else 0.0.

    Args:
        cutoff: Number of gameweeks to include with full weight (1.0).
        horizon: Total number of fixture weeks in the temporal window (>= 1).

    Returns:
        List of float weights for t = 0 .. horizon-1.

    Raises:
        ValueError: If horizon < 1 or cutoff < 0.
    """
    if horizon < 1:
        raise ValueError(f"Horizon must be >= 1, got {horizon}")
    if cutoff < 0:
        raise ValueError(f"Cutoff must be >= 0, got {cutoff}")

    return [1.0 if t < cutoff else 0.0 for t in range(horizon)]


def interpolate_gradient(start: float, end: float, steps: int) -> List[float]:
    """Generates an evenly spaced gradient of parameter values from start to end.

    Args:
        start: Starting parameter value.
        end: Ending parameter value.
        steps: Total number of gradient steps (must be >= 2).

    Returns:
        List of float parameter values rounded to 6 decimal places.

    Raises:
        ValueError: If steps < 2.
    """
    if steps < 2:
        raise ValueError(f"Steps must be >= 2, got {steps}")

    step_size = (end - start) / (steps - 1)
    return [round(start + i * step_size, 6) for i in range(steps)]


def generate_scenario_signature(
    model: str, param: float, form_weight: float | None = None
) -> str:
    """Generates a compact, standardized Scenario Signature for column headers.

    Examples:
        'exponential', 0.75 -> 'EXP:0.75'
        'linear', 0.2 -> 'LIN:0.20'
        'step', 3.0 -> 'STEP:3'
        'linear', 0.2, form_weight=0.7 -> 'LIN:0.20_FW:0.7'

    Args:
        model: Decay model name ('linear', 'exponential', 'step').
        param: Parameter value (decay_rate, slope, or horizon cutoff).
        form_weight: Optional form factor weight modifier.

    Returns:
        Compact signature string.
    """
    clean_model = model.strip().lower()
    if clean_model in ("exponential", "exp"):
        prefix = "EXP"
        param_str = f"{param:.2f}"
    elif clean_model in ("linear", "lin"):
        prefix = "LIN"
        param_str = f"{param:.2f}"
    elif clean_model in ("step", "horizon"):
        prefix = "STEP"
        param_str = f"{int(param)}"
    else:
        prefix = clean_model.upper()
        param_str = f"{param:.2f}"

    sig = f"{prefix}:{param_str}"
    if form_weight is not None:
        sig += f"_FW:{form_weight:.1f}"
    return sig
