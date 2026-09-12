# RFC-011: The Retrospective Lens (Fixture-Adjusted Form)
**STATUS: PLANNED**

## 1. Abstract
Currently, the Chimera utilizes a raw `Form Factor` (calculated from points scored over a lookback period). This "blind" approach treats all points as equal, regardless of the opposition's strength. RFC-011 proposes the **Retrospective Lens**: a mechanism to weight previous points by the difficulty of the fixtures in which they were scored. This transforms "Raw Form" into "Contextual Efficiency," allowing the solver to distinguish between players who "stat-padded" against weak defenses and players who maintained production against elite opposition.

## 2. The Problem: The "Stat-Padding" Fallacy
Raw points are a lagging indicator that can be misleading. A player scoring 10 points against a bottom-three defense is not necessarily as "in-form" as a player scoring 6 points against the league leaders. 

By ignoring the **Historical FDR**, the Chimera is susceptible to:
- **Chasing Ghost Form:** Overvaluing players whose recent success is a product of a "soft" schedule.
- **Under-valuing Suppressed Elites:** Ignoring players who are performing well relative to a brutal schedule, but whose raw totals are low.

## 3. Proposed Solution: The Retrospective Lens
Implement a weighting mechanism that adjusts points based on the FDR of the fixture they were earned in.

### 3.1 The Adjusted Form Calculation
Instead of a simple average of points, the `Adjusted_Form` is calculated as the sum of points weighted by the corresponding historical FDR.

$$\text{Adjusted Form} = \sum_{g=1}^{\text{lookback}} (\text{Points}_g \times \text{FDR}_{\text{past}_g})$$

*Note: If FDR is expressed as a high-magnitude scalar (e.g., 1000-1300), it should be normalized (e.g., $\text{FDR} / 1000$) to prevent the form factor from completely dominating the equation.*

### 3.2 The Efficiency Ratio (Alternative)
As an alternative or augmentation, we can track **Form Efficiency**:
$$\text{Efficiency} = \frac{\text{Actual Points}}{\text{Expected Points for that FDR}}$$
Players with an efficiency $> 1.0$ are "outperforming their fixtures," providing a stronger signal of genuine form.

## 4. Operational Integration

### 4.1 Data Requirements
The pipeline must be updated to maintain a record of the FDR for each gameweek within the `form_lookback_weeks` window. This requires the `process_fixtures_html.py` logic to archive historical FDRs.

### 4.2 Equation Update
The `Final Score` equation is updated as follows:
$$\text{Final Score} = \frac{\text{PP} + \text{SPP} + (\text{Adjusted Form} \times \text{Weight})}{\text{Effective FDR}}$$

### 4.3 Validation via Scenario Forge
The impact of the Retrospective Lens will be audited using the existing `bamf forge` infrastructure. By running a binary scenario matrix:
- **Scenario A:** `form_model = "raw"`
- **Scenario B:** `form_model = "retrospective"`
The resulting **Stability Grid** will highlight "Form Frauds"—players who are dropped when the lens is applied.

## 5. Strategic Value
- **The "Fraud" Detector:** Rapidly identifies players whose form is a byproduct of a weak schedule.
- **The "Sleeper" Finder:** Identifies elite assets who are "due" for a breakout because they've been performing well despite a brutal run.
- **Increased Robustness:** Reduces the volatility of the `form_factor_weight` by grounding the recency bias in historical reality.
