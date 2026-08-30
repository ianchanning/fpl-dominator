# RFC-004: Wildcard Trigger Protocol

## 1. Objective
Establish a mathematical trigger for the "Wildcard" (total squad reset) to avoid the "Sunk Cost Fallacy" and prevent the squad from getting trapped in a local minimum.

## 2. The Wildcard as a Financial Option
The Wildcard is mathematically treated as an **American Call Option** with an expiration date at the GW19 deadline.

### 2.1 Option Value Components
- **Intrinsic Value:** The immediate point jump gained by resetting the squad today ($\text{Divergence Delta}$).
- **Time Value ($\Theta$-Decay):** The future flexibility to respond to unpredictable injury crises, tactical collapses, or managerial shifts.
- **The Exercise Rule:** Trigger the Wildcard only if:
  $$\text{Intrinsic Value} > \text{Time Value} + \text{Cost of Multi-Period Hits}$$

## 3. The "3-Path Gauntlet" Evaluation
The decision to trigger the Wildcard is determined by executing a multi-path graph evaluation over a horizon $H=5$:

### 3.1 The Paths
- **Path A (Status Quo):** Optimize trajectory with 0 hits allowed (rolling FTs only).
- **Path B (Manual Migration):** Optimize trajectory allowing targeted hits (up to a hard cap, e.g., $-12$ pts).
- **Path C (Wildcard Reset):** Reset $x_{i,0}$ to a blank slate, 0 hit penalty, solve for global optimum.

### 3.2 The Automated Decision Rule
The Wildcard is triggered if:
$$\left( \mathbb{E}[\text{Path C}] - \max(\mathbb{E}[\text{Path A}], \mathbb{E}[\text{Path B}]) \right) \ge \Delta_{\text{threshold}}(t)$$

**Dynamic Threshold $\Delta_{\text{threshold}}(t)$:**
To account for the fading "Time Value" ($\Theta$), the threshold decays as the GW19 deadline approaches:
- **Early Season (GW2):** $\sim 30$ points.
- **Late Season (GW16):** $\sim 12$ points.

## 4. The International Break Alpha
During international break windows, the Wildcard provides **Price Liquidity Alpha**. 
- **Equity Banking:** Playing the Wildcard early in the break allows for the strategic acquisition of rising assets before their prices climb, banking team equity (budget) that would be unavailable in a standard transfer window.

## 5. Implementation Strategy
- **Module:** `src/fpl_dominator/wildcard_evaluator.py`.
- **Process:** Compare expected returns of the 3-Path Gauntlet against the $\Delta_{\text{threshold}}(t)$.
- **Output:** Recommendation: `HOLD` or `FIRE WILDCARD`.
