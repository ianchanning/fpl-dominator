# RFC-007: Early-Season Liquidity & Dynamic Team Value Arbitrage

## 1. Objective
Incorporate expected transfer market price momentum into the linear optimization objective during the first 8 gameweeks, maximizing franchise purchasing power for subsequent Wildcard deployments.

## 2. The Problem: Capital Starvation
FPL is a game of compound capital. Managers who ignore price momentum find themselves with a static £100.0m squad in November, while optimal managers wield £104.5m in purchasing power, enabling an extra premium asset in their starting XI.

## 3. Mathematical Logic: Dual-Objective Points + Equity Maximization

### 3.1 Net Price Velocity ($\Delta \widehat{\text{Price}}$)
Using net transfer velocity data ripped via `bamf rip transfer-trends`, we predict the 7-day price delta $\Delta \widehat{\text{Price}}_{i} \in \{-0.2, -0.1, 0.0, +0.1, +0.2\}$.

### 3.2 The Dual-Objective Formulation (GW1–GW8)
$$
\max \sum_{t=1}^{H} \gamma^{t-1} \left( \sum_{i \in \text{XI}_t} \text{Points}_{i,t} + \lambda(t) \cdot \Delta \widehat{\text{Price}}_{i,t} \right) - \text{Penalty}(\text{Hits})
$$
- **Dynamic Liquidity Weight $\lambda(t)$:**
  $$
  \lambda(t) = \max\left(0, 0.75 \times \frac{8 - t}{8}\right)
  $$
  *(High price-growth weighting in GW1–GW4, fading to pure point optimization by GW8).*

## 4. Implementation Manifest
- **Module:** `src/fpl_dominator/update_prices.py` (Enhanced with momentum velocity scraper).
- **Integration:** Directly modifies Pyomo objective coefficients in `src/fpl_dominator/commander.py`.
