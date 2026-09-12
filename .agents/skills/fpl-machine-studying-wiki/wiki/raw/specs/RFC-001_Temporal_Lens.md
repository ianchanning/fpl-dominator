# RFC-001: Temporal Lens and Future Discounting

**STATUS: IMPLEMENTED / ACTIVE**

## 1. Objective
Eliminate the "flat" view of the future. The Chimera must prioritize immediate performance over distant potential to better reflect the volatility and urgency of FPL.

## 2. The Temporal Discounting Model
Instead of calculating a simple arithmetic mean for fixture difficulty over a horizon, we apply a weighted decay.

### 2.1 Weights Configuration
Weights are defined in `config.yaml` under `temporal_discounting`.
Example weights: `[1.0, 0.8, 0.6, 0.4, 0.2]` for the next 5 gameweeks.

### 2.2 The Weighted Average Formula
The `Effective_FDR_Horizon_5GW` for both Attack (A) and Defence (D) is calculated as:

$$\text{Weighted FDR} = \frac{\sum_{i=1}^{5} (w_i \times \text{FDR}_i)}{\sum_{i=1}^{5} w_i}$$

where $w_i$ is the weight for gameweek $i$ and $\text{FDR}_i$ is the fixture difficulty for that week.

## 3. System Implementation
- **Engine:** `grand_synthesis.py` is responsible for loading weights and applying them to the `fdr_horizon` calculation.
- **Data Transformation:** The logic groups fixtures by team and applies the weighted summation to derive the final effective FDR used by the solver.
