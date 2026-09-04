# RFC-008: The Scenario Forge (Config Sensitivity Analysis)

## 1. Abstract
Currently, the Chimera is executed against a single `config.yaml` state. This creates a "single point of failure" where a slight miscalibration of `form_factor_weight` or `red_zone_threshold` can lead to sub-optimal squad selection. The Scenario Forge introduces a mechanism to run the optimization engine across a multi-dimensional matrix of configuration parameters—now utilizing functional parameterization for temporal decay—to identify "Robust Assets."

## 2. The Problem: The "Tweak and Pray" Cycle
The user currently modifies `config.yaml` and runs `bamf finalize`. This is a manual, linear process that lacks:
- **Sensitivity Analysis:** No understanding of how a $\pm 10\%$ change in `form_factor_weight` affects the XI.
- **Strategic Personas:** No way to compare different "Decay Philosophies" (e.g., Linear vs. Exponential).
- **Confidence Metrics:** No way to know if a player is a "Lock" or a "Coin-flip."

## 3. Proposed Solution: The Forge
Implement a new command `bamf forge` that accepts a set of parameter ranges or a list of "Model Profiles."

### 3.1 Functional Parameterization
Instead of static arrays, the Forge will utilize weight generator functions:
- **Linear:** $W(t) = 1.0 - (t \times \text{slope})$
- **Exponential:** $W(t) = \text{decay\_rate}^t$
- **Step:** $W(t) = 1.0 \text{ if } t < \text{horizon else } 0.0$

### 3.2 Operational Logic
The Forge will:
1. **Define a Parameter Matrix:**
   - e.g., `decay_model`: `["linear", "exponential"]`
   - e.g., `form_factor_weight`: `[0.5, 0.7, 0.9]`
   - e.g., `slope/decay_rate`: `[0.1, 0.5]`
2. **Execute Parallel Solves:** Run the Chimera pipeline for every combination in the Cartesian product of these parameters.
3. **Aggregate Selection Frequency:** Calculate the percentage of times each player is selected across all successful solves.

### 3.3 The "Robustness" Metric
A player's **Robustness Score** $R$ is defined as:
$$R = \frac{\text{Count of selections across all scenarios}}{\text{Total number of successful solves}}$$

## 4. Visualization & Output (The Stability Matrix)
To avoid information overload, the Forge will produce a **Diff-First** visualization:

- **The Stability Grid:** A compact table where the Y-axis is squad position and the X-axis consists of **Scenario Signatures** (e.g., `EXP:0.5`).
- **Noise Suppression:** 
    - Bench players are hidden unless they change across scenarios.
    - Static values (prices, etc.) are suppressed.
- **The Weight Registry (Source of Truth):** A footer mapping each Scenario Signature to the full computed weight array (e.g., `EXP:0.5` $\rightarrow$ `[1.0, 0.5, 0.25, 0.12, 0.06]`).

## 5. Implementation Plan
1. **Phase 1: The Weight Generator.** Implement the `linear`, `exponential`, and `step` functions to generate `fixture_weights`.
2. **Phase 2: The Runner.** Create a wrapper that overrides `config.yaml` values via environment variables.
3. **Phase 3: The Aggregator.** Generate the frequency table, stability grid, and weight registry.

## 5. Impact on the "Frenchman"
By identifying the **Ironclad Assets**, we remove the emotional noise of "trying a different config" and focus on the mathematical truth. We stop chasing ghosts and start deploying a squad backed by a statistical ensemble.
