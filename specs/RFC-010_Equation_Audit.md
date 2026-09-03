# RFC-010: The Equation Audit (Final Score Stress-Testing)

## 1. Abstract
The "Final Score" equation is the heart of the Chimera, but its mathematical structure has not been rigorously stress-tested. This RFC proposes a framework to audit the current division-based scoring model against alternative mathematical structures to determine if we are unnecessarily penalizing high-quality assets in difficult fixtures.

## 2. Current Equation (The Baseline)
$$\text{Final Score} = \frac{\text{PP} + \text{SPP} + (\text{Form Factor} \times \text{Weight})}{\text{Effective FDR}}$$

**Critique:** The inverse-linear relationship created by the divisor means that a moderate increase in FDR can nullify a significant increase in expected points (PP).

## 3. Proposed Alternative Models

### 3.1 The "Penalty" Model (Subtraction)
$$\text{Final Score} = (\text{PP} + \text{SPP} + (\text{Form Factor} \times \text{Weight})) - (\text{Effective FDR} \times \text{Penalty\_Coefficient})$$
- **Logic:** Treat the FDR as a cost/penalty rather than a scalar. This prevents the "Divisor Death" where a high FDR annihilates the score.

### 3.2 The "Multiplicative" Model (Weighted Factor)
$$\text{Final Score} = (\text{PP} + \text{SPP} + (\text{Form Factor} \times \text{Weight})) \times \text{FDR\_Modifier}$$
- **Logic:** Use a multiplier (e.g., 0.7 to 1.3) based on FDR. This maintains the relative strength of the PP while still shifting the preference.

## 4. The Audit Process
The "Equation Audit" will be implemented as a specialized version of the Scenario Forge:
1. **Parallel Execution:** Run the solver using the Baseline, Penalty, and Multiplicative models on the same data.
2. **Selection Divergence:** Identify players who are "Dropped" by the Baseline but "Picked" by the Alternatives.
3. **Reality Check:** Compare these "dropped" players against actual performance data (backtesting) to see if the Baseline was too conservative.

## 5. Goal
To determine if a structural change to the `Final Score` equation increases the "Prophetic Accuracy" of the Chimera and prevents us from over-rotating based on FDRfear.
