# Price Change Reality Alignment & Treasury Mechanics

## 1. The Sovereign Law
Reconcile market price shifts against actual squad selling values ($P_{\text{sell}} = P_{\text{buy}} + \lfloor \frac{P_{\text{current}} - P_{\text{buy}}}{2} \rfloor$) and bank treasury before running the solver to ensure mathematical feasibility of proposed transfers.

---

## 2. The Trigger & Context
In Fantasy Premier League, player prices fluctuate daily based on transfer volume:
- **The Profit Division Trap:** When a player you own rises in price, you only capture $50\%$ of the profit (rounded down to $0.1\text{m}$). If you bought a player at $6.0\text{m}$ and they rise to $6.3\text{m}$, your selling price is $6.1\text{m}$, not $6.3\text{m}$.
- **The Budget Infeasibility Shock:** If the solver uses current market prices for owned squad members instead of actual selling prices, it may propose a set of transfers that exceeds your actual available purchasing power, crashing the weekly plan when executed on the official site.
- **The Solution (`update_prices.py`):** The `squad.csv` dump ripped from the official FPL transfers page contains exact `purchase_price`, `selling_price`, and `bank` figures. `update_prices.py` reconciles market statistics with your exact treasury realities.

---

## 3. Dynamic Chaos vs. Typed Mathematical Truth

| Dimension | Naive Market-Price Assumption | Reality-Aligned Treasury Engine |
| :--- | :--- | :--- |
| **Squad Asset Valuation** | Evaluated at current market price $P_{\text{now}}$. | Evaluated at true liquidated selling price $P_{\text{sell}}$. |
| **Available Budget** | Theoretical $100.0\text{m}$. | **Exact Liquid Purchasing Power:** $\text{Bank} + \sum_{i \in \text{Transferred Out}} P_{\text{sell}, i}$. |
| **Execution Feasibility** | Risk of $0.1\text{m}$ shortfall causing failed official transfers. | **100% Guaranteed Feasibility:** Mathematical certainty that proposed moves fit within bank balance. |

---

## 4. The Implementation Pattern (`update_prices.py`)

```python
import pandas as pd

def align_treasury_reality(market_df: pd.DataFrame, squad_df: pd.DataFrame, bank_balance: float) -> tuple[pd.DataFrame, float]:
    """
    Overwrites market prices for currently owned players with their exact selling values
    and calculates total available purchasing power.
    """
    merged = market_df.copy()
    
    # Map selling price for owned players
    selling_price_map = squad_df.set_index("player_name")["selling_price"].to_dict()
    
    merged["Effective_Price"] = merged["player_name"].map(
        lambda name: selling_price_map.get(name, merged.loc[merged["player_name"] == name, "Price"].values[0])
    )
    
    total_liquid_treasury = bank_balance + squad_df["selling_price"].sum()
    
    return merged, total_liquid_treasury
```
