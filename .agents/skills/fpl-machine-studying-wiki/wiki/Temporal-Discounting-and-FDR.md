# Temporal Discounting & Weighted Fixture Difficulty (FDR)

## 1. The Sovereign Law
Calculate multi-gameweek fixture difficulty ratings using temporal decay weighting ($w = [1.0, 0.8, 0.6, 0.4, 0.2]$) rather than flat arithmetic means: near-term fixtures have exponentially higher impact on transfer expected value than distant fixtures.

---

## 2. The Formulation & Trigger Context
In early versions of BAMF Dominator, fixture horizon metrics used naive arithmetic means over 5 Gameweeks:
$$\text{Naive\_FDR} = \frac{1}{5} \sum_{t=1}^5 \text{FDR}_t$$

### The Flaw of Equal Importance
- **The Immediacy Trap:** A team facing Manchester City away (FDR 5) in GW30 followed by four easy fixtures (FDR 2, 2, 2, 2) has the exact same average FDR ($2.6$) as a team facing four easy fixtures first (FDR 2, 2, 2, 2) followed by Manchester City in GW34!
- **Transfer Horizon Reality:** In FPL, free transfers are accumulated weekly. Buying a player who blanks or gets benched in the immediate next Gameweek causes immediate rank drops and burns future transfers to fix. Immediate difficulty matters far more than difficulty 5 weeks out.

---

## 3. Dynamic Chaos vs. Typed Mathematical Truth

| Dimension | Flat Arithmetic Mean (`.mean()`) | Temporal Discounting Horizon |
| :--- | :--- | :--- |
| **Time Preference** | Timeless; treats Gameweek $t+5$ identically to Gameweek $t+1$. | **Present-Biased:** Near-term fixtures weighted up to $5\times$ higher than distant fixtures. |
| **Transfer Agility** | Encourages holding players through tough immediate fixtures. | Recommends tactical short-term punts and timely exits before fixture swings. |
| **Mathematical Formula** | $\bar{F} = \frac{1}{H} \sum_{t=1}^H F_t$ | $F_{\text{eff}} = \frac{\sum_{t=1}^H w_t F_t}{\sum_{t=1}^H w_t}$ with $w = [1.0, 0.8, 0.6, 0.4, 0.2]$. |

---

## 4. The Implementation Pattern (`grand_synthesis.py`)

```python
import numpy as np
import pandas as pd

def calculate_temporal_fdr(fixtures_df, weights=None):
    """
    Calculates weighted FDR for each team across upcoming horizon.
    Default weights: [1.0, 0.8, 0.6, 0.4, 0.2] for 5-GW horizon.
    """
    if weights is None:
        weights = [1.0, 0.8, 0.6, 0.4, 0.2]

    weights = np.array(weights[:5])
    weight_sum = weights.sum()

    team_fdr_scores = {}

    for team, group in fixtures_df.groupby("Team"):
        # Sort chronologically by gameweek
        sorted_fixtures = group.sort_values("GW").head(5)
        
        attack_fdr = sorted_fixtures["FDR_Attack"].values
        defense_fdr = sorted_fixtures["FDR_Defense"].values

        # Ensure correct array length alignment
        n = len(attack_fdr)
        if n == 0:
            continue
            
        current_weights = weights[:n]
        current_sum = current_weights.sum()

        weighted_attack = np.dot(attack_fdr, current_weights) / current_sum
        weighted_defense = np.dot(defense_fdr, current_weights) / current_sum

        team_fdr_scores[team] = {
            "FDR_A_Horizon_5GW": weighted_attack,
            "FDR_D_Horizon_5GW": weighted_defense
        }

    return pd.DataFrame.from_dict(team_fdr_scores, orient="index")
```
