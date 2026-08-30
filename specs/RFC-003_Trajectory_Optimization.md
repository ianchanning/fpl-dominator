# RFC-003: Trajectory Optimization and Transition Friction

## 1. Objective
Transform the BAMF Dominator from a "Snapshot Optimizer" into a "Trajectory Optimizer." The system must find the most efficient path to an ideal state over a rolling horizon $H$, accounting for transfer costs, budget liquidity, and the option value of banked transfers.

## 2. The Problem: Transition Friction & Budget Liquidity
The cost of changing players is non-linear (1 free transfer, then -4 per additional). Furthermore, the ability to upgrade a player's price is constrained by the current bank balance and the number of transfers available. 

**The Budget Pivot:** A manager can only increase a position's spend if they have spare cash or if they use multiple transfers to "downgrade" another position in the same window.

## 3. Mathematical Formulation (Linearized)

### 3.1 State-Transition Variables
For every player $i$ and time step $t \in \{1 \dots H\}$, we define binary variables:
- $x_{i,t} \in \{0, 1\}$: Player $i$ is owned in GW $t$.
- $u_{i,t} \in \{0, 1\}$: Player $i$ is bought in GW $t$.
- $v_{i,t} \in \{0, 1\}$: Player $i$ is sold in GW $t$.

**Constraint:** 
$$x_{i,t} = x_{i,t-1} + u_{i,t} - v_{i,t} \quad \forall i, \forall t$$

### 3.2 Temporal Budget Tracking
Instead of a static budget constraint, we track the bank balance as a state variable:
$$\text{Bank}_t = \text{Bank}_{t-1} + \sum_{i} (v_{i,t} \cdot \text{Price}_{i,t}) - \sum_{j} (u_{j,t} \cdot \text{Price}_{j,t})$$
**Constraint:** $\text{Bank}_t \ge 0 \quad \forall t$

This ensures that "Premium Pivots" (bringing in a more expensive player) are only possible if the solver sells enough value in the same window to keep the bank non-negative.

### 3.3 Linearized Hit Penalty
To handle the transfer penalty without non-linear functions, we introduce a continuous slack variable $H_t \ge 0$ for each gameweek $t$:

$$\sum_{i} u_{i,t} - \text{FT}_t \le H_t$$

The total penalty in the objective function is then:
$$\text{Total Penalty} = \sum_{t=1}^{H} 4.0 \cdot H_t$$

### 3.4 Banked Free Transfer (FT) Dynamics
Following the current ruleset (max 5 FTs), the transfer allowance evolves recursively:
$$\text{FT}_{t+1} = \min(5, \max(1, \text{FT}_t - \sum_i u_{i,t} + 1))$$

**Strategic Note:** The solver treats banked transfers as **Positive Option Value**, weighing the immediate point gain of a transfer against the utility of having more free transfers in future high-volatility windows or for complex budget pivots.

## 4. Objective Function: $\gamma$-Discounted Net Gain
To account for forecast variance over the horizon $H$, we apply a discount parameter $\gamma \in [0.88, 0.92]$.

$$\text{Maximize } \text{Net Trajectory Gain} = \sum_{t=1}^{H} \left( \gamma^{t-1} \cdot \mathbb{E}[\text{Points}_t] \right) - \sum_{t=1}^{H} (4.0 \cdot H_t)$$

## 5. Implementation Strategy
- **Solver:** Pyomo $\rightarrow$ GLPK.
- **Input:** Current Squad ($x_{i,0}$), current Bank ($\text{Bank}_0$), and current FT bank ($\text{FT}_1$).
- **Horizon:** Rolling $H=3$ to $5$ gameweeks.
