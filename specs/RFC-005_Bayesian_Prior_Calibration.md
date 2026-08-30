# RFC-005: Bayesian Prior Calibration & Managerial Regime Adaptation (MRV)

## 1. Objective
Eliminate reliance on stale historical point totals and prevent $N=1$ Poisson overfitting by decomposing player value into **Underlying Process Metrics** (npxG, xA, Box Touches, Set-Piece Dominance) and updating them via **Exponential Bayesian Shrinkage** parameterized by **Managerial Regime Vectors (MRV)**.

## 2. The Problem: Tactical Regime Shifts
In the 2026/27 season, managerial changes (e.g., Man City, Liverpool) fundamentally alter player tactical roles. 
- Historical points from 2025/26 reflect obsolete systems.
- Early gameweek points ($N \le 4$) suffer from high variance and small-sample illusion.
- The solver requires an adaptive prior that bridges the gap between pre-season structural expectations and realized 2026 tactical reality.

## 3. Mathematical Logic: Fast-Decaying Bayesian Priors

### 3.1 Decomposition of Underlying Rates
Instead of predicting raw FPL points $P$, we predict per-90 underlying rates:
$$\mathbf{r}_i = [\text{npxG}_{90}, \text{xA}_{90}, \text{xGC}_{90}, \text{SCA}_{90}]^T$$

### 3.2 The Managerial Regime Vector (MRV) Modifier
Each club's new managerial setup is assigned a tactical profile vector $\mathbf{W}_{\text{mgr}} \in \mathbb{R}^k$ (Press Line Height, Directness, Fullback Inversion, Cross Volume):
$$\mathbf{r}_{i, \text{prior}} = \mathbf{r}_{i, \text{baseline}} \odot (1 + \mathbf{W}_{\text{mgr}} \cdot \mathbf{v}_{\text{role}})$$

### 3.3 Exponential Bayesian Updating Formula
As gameweeks accumulate ($t = 1, 2, \dots, T$), the expected rate $\hat{\mathbf{r}}_{i,t}$ is updated dynamically:
$$\hat{\mathbf{r}}_{i,t} = (1 - \alpha)^t \cdot \mathbf{r}_{i, \text{prior}} + \sum_{k=1}^t \alpha (1 - \alpha)^{t-k} \cdot \mathbf{x}_{i,k}$$
- **Hyperparameter $\alpha$ (Learning Rate):** Set to $\alpha = 0.30$ during GW1–GW4 (accelerated adaptation), decaying to $\alpha = 0.12$ by GW8 (stable equilibrium).

## 4. Implementation Manifest
- **Module:** `src/fpl_dominator/bayesian_priors.py`
- **Inputs:** Raw FFS match underlying metrics, historical baseline rates, `manager_profiles.json`.
- **Output:** Enriched, regularized per-90 rates feeding directly into `fpl_master_database_FINAL_v5.csv`.
