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
