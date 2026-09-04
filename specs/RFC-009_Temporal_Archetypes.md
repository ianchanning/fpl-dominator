# RFC-009: Temporal Gradients (Selection Stability Analysis)

## 1. Abstract
Rather than utilizing static arrays for `fixture_weights`, RFC-009 proposes a **Gradient Analysis** approach based on functional parameterization. By interpolating the parameters of a chosen decay model (Linear, Exponential, or Step), we can map the "Survival Curve" of each player. This reveals the exact point where a player's value collapses as the strategic horizon shrinks.

## 2. The Concept: Parameter Interpolation
The Chimera will execute a series of solves by interpolating the *parameters* of a decay function.

### 2.1 Decay Models
- **Linear:** $W(t) = 1.0 - (t \times \text{slope})$
- **Exponential:** $W(t) = \text{decay\_rate}^t$
- **Step:** $W(t) = 1.0 \text{ if } t < \text{horizon else } 0.0$

### 2.2 The Gradient Path
The Forge will compute $N$ steps between two parameter extrema.
- **Example (Exponential):** Interpolating `decay_rate` from $1.0$ (Eternalist) to $0.0$ (Pure Sniper).
- **Example (Step):** Interpolating `horizon` from $5$ (Full Horizon) to $1$ (Immediate Only).

For $N=4$, an exponential gradient produces:
1. `decay_rate = 1.0` $\rightarrow$ `[1, 1, 1, 1, 1]`
2. `decay_rate = 0.75` $\rightarrow$ `[1, 0.75, 0.56, 0.42, 0.31]`
3. `decay_rate = 0.5` $\rightarrow$ `[1, 0.5, 0.25, 0.12, 0.06]`
4. `decay_rate = 0.25` $\rightarrow$ `[1, 0.25, 0.06, 0.01, 0.00]`
5. `decay_rate = 0.0` $\rightarrow$ `[1, 0, 0, 0, 0]`

## 3. The "Survival Curve" Analysis
The output is a **Selection Window** based on the parameter gradient:

- **The Immortals:** Selected across the entire parameter range. These are the mathematically mandatory picks.
- **The Horizon-Dependents:** Selected only when the decay is slow (e.g., `decay_rate > 0.6`).
- **The Pure Punts:** Selected only when the decay is extreme (e.g., `decay_rate < 0.2`).

## 4. Operational Integration & Visualization
This logic is integrated into `bamf forge`:
- **Input:** `--model [linear|exponential|step]`
- **Input:** `--param_range "[start, end]"` (e.g., `[1.0, 0.0]`)
- **Input:** `--steps 5`
- **Visualization:** 
    - **Stability Grid:** Players mapped against **Scenario Signatures** (e.g., `EXP:0.5`) to identify divergence points.
    - **Weight Registry:** A footer mapping each signature to the full computed weight array to provide absolute mathematical traceability.

## 5. Strategic Value
This removes the guesswork of "array picking." We can now determine if a player's presence in the squad is a result of the *model type* (Linear vs Exponential) or the *decay intensity* (Rate/Slope).
