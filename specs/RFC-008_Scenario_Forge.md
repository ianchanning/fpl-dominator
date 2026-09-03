# RFC-008: The Scenario Forge (Config Sensitivity Analysis)

## 1. Abstract
Currently, the Chimera is executed against a single `config.yaml` state. This creates a "single point of failure" where a slight miscalibration of `form_factor_weight` or `thrift_factor` can lead to sub-optimal squad selection. The Scenario Forge introduces a mechanism to run the optimization engine across a multi-dimensional matrix of configuration parameters to identify "Robust Assets"—players who persist across multiple viable strategic personas.

## 2. The Problem: The "Tweak and Pray" Cycle
The user currently modifies `config.yaml` and runs `bamf finalize`. This is a manual, linear process that lacks:
- **Sensitivity Analysis:** No understanding of how a $\pm 10\%$ change in `form_factor_weight` affects the XI.
- **Strategic Personas:** No way to compare a "Safe/Conservative" setup (low form bias, high thrift) vs. an "Aggressive/Chaos" setup (high form bias, low thrift).
- **Confidence Metrics:** No way to know if a player is a "Lock" or a "Coin-flip."

## 3. Proposed Solution: The Forge
Implement a new command `bamf forge` (or `bamf scenario`) that accepts a set of parameter ranges rather than static values.

### 3.1 Operational Logic
The Forge will:
1. **Define a Parameter Matrix:**
   - e.g., `form_factor_weight`: `[0.5, 0.7, 0.9]`
   - e.g., `thrift_factor`: `[0.001, 0.01]`
   - e.g., `red_zone_limit`: `[4, 5, 6]`
2. **Execute Parallel Solves:** Run the Chimera pipeline for every combination in the Cartesian product of these parameters.
3. **Aggregate Selection Frequency:** Calculate the percentage of times each player is selected across all successful solves.

### 3.2 The "Robustness" Metric
A player's **Robustness Score** $R$ is defined as:
$$R = \frac{\text{Count of selections across all scenarios}}{\text{Total number of successful solves}}$$

- **$R \approx 1.0$**: **Ironclad Asset.** This player is mathematically dominant regardless of the strategy.
- **$0.5 < R < 0.8$**: **Strategic Asset.** This player is strong but dependent on specific biases (e.g., high form weight).
- **$R < 0.3$**: **Opportunistic Asset.** A "punt" that only works in specific, narrow configurations.

## 4. Implementation Plan (The Surgical Path)
To avoid the "Enormous RFC" trap, we implement this in three surgical strikes:

1. **Phase 1: The Runner.** Create a wrapper script that can override `config.yaml` values via environment variables or a temporary JSON override before calling the existing solve logic.
2. **Phase 2: The Aggregator.** A simple post-processing script that reads multiple `squad_prophecy.md` (or internal results) and generates a frequency table.
3. **Phase 3: The Forge CLI.** Integrate into `bamf.py` as a first-class command with a clean output table.

## 5. Impact on the "Frenchman"
By identifying the **Ironclad Assets**, we remove the emotional noise of "trying a different config" and focus on the mathematical truth. We stop chasing ghosts and start deploying a squad backed by a statistical ensemble.
