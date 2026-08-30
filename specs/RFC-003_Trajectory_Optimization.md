# RFC-003: Trajectory Optimization and Transition Friction

## 1. Objective
Transform the BAMF Dominator from a "Snapshot Optimizer" (finding the best squad for a single moment) into a "Trajectory Optimizer" (finding the most efficient path to an ideal state over multiple gameweeks).

## 2. The Problem: Transition Friction
The current Chimera solver ignores the FPL cost of changing players. In reality, players are not free; they cost points (-4 per additional transfer).

## 3. Proposed Logic: The Net Gain Equation
The solver must optimize for `Net Gain` over a rolling horizon (e.g., $H = 3$ to $5$ gameweeks).

$$\text{Net Gain} = \left( \sum_{gw=n}^{n+H} \text{Points}(\text{Target Squad}) - \sum_{gw=n}^{n+H} \text{Points}(\text{Current Squad}) \right) - \text{Transfer Penalty}$$

### 3.1 Transfer Penalty Calculation
- **Free Transfer:** 1 transfer per week is free. If not used, it rolls over to a maximum of 2 (depending on current FPL rules).
- **Hits:** Every transfer beyond the free allowance incurs a $-4$ point penalty.
- **The Formula:** $\text{Transfer Penalty} = (\max(0, \text{Transfers} - \text{Free Allowance})) \times 4$.

## 4. Implementation Strategy
- **Input Requirements:** The solver needs the `Current Squad` as a hard constraint/input.
- **Decision Variable:** The solver must decide not just *who* to have, but *whether to transfer* based on the ROI of the point gain vs. the hit.
- **Horizon Analysis:** Compare the trajectory of the current squad vs. the trajectory of the optimized squad over the next $H$ weeks.
