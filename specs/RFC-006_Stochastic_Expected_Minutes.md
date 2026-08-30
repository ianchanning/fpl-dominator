# RFC-006: Stochastic Expected Minutes ($\text{xMins}$) & Ruin-Resistant Monte Carlo Simulation

## 1. Objective
Transform the deterministic MILP objective function into a **Stochastic / Risk-Adjusted Optimizer** by explicitly modeling rotation probability ($\text{xMins}$) and applying **Conditional Value at Risk (CVaR)** penalties to eliminate high-downside bench traps.

## 2. The Problem: Deterministic Point Hallucination
Standard linear programming evaluates an asset at nominal expected points $\mathbb{E}[P]$. A player with an expected 7.0 points who starts 50% of games is treated identically to a nailed 7.0-point talisman who starts 100% of games. When the rotation hammer falls, the squad absorbs a 0-point penalty and collapses.

## 3. Mathematical Logic: Stochastic Simulation & Downside Penalization

### 3.1 Expected Minutes Distribution ($\text{xMins}$)
Each player's minutes are modeled as a mixture distribution:
$$
\text{Mins}_i \sim (1 - p_{\text{start}}) \cdot \text{SubCameo}(\lambda) + p_{\text{start}} \cdot \text{Beta}(\alpha_i, \beta_i) \times 90
$$
where $p_{\text{start}}$ is determined by injury status, turnaround days, and European fixture congestion flags.

### 3.2 Pre-Solver Monte Carlo Gauntlet
Before calling GLPK (`glpsol`), `src/fpl_dominator/stochastic_sim.py` runs $K = 5,000$ simulated gameweek scenarios:
1. Sample player minutes $\text{Mins}_{i, k}$.
2. Sample attacking/defensive events from Poisson distributions parameterized by $\hat{\mathbf{r}}_{i, t} \times (\text{Mins}_{i, k} / 90)$.
3. Compute simulated score distribution $S_{i} = \{s_{i, 1}, s_{i, 2}, \dots, s_{i, K}\}$.

### 3.3 The Risk-Adjusted Objective Function
The Pyomo solver optimizes the **Downside-Penalized Expected Score**:
$$
\text{Objective}_i = \mathbb{E}[S_i] - \kappa \cdot \text{CVaR}_{\beta}(S_i) \cdot \mathbb{P}(\text{Mins}_i < 60)
$$
- **$\kappa$ (Ruin Aversion Parameter):** Set to $\kappa = 0.50$ for starting XI assets, ensuring that rotation traps with high ceiling but low floor are ruthlessly rejected.

## 4. Implementation Manifest
- **Module:** `src/fpl_dominator/stochastic_sim.py`
- **CLI Trigger:** `bamf gauntlet --stochastic --samples=5000`
- **Output:** `stochastic_player_scores.csv` ingested directly by `commander.py`.
