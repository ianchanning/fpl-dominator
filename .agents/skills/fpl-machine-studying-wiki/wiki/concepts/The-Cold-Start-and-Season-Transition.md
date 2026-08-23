# The Cold Start & Season Transition Protocol

## 1. The Sovereign Law
At the inception of a new season (GW1), eliminate the Total Points zero-point singularity by blending decaying prior-season performance baselines with current fixture difficulty and unconstrained greenfield budget optimization.

---

## 2. The Formulation & Trigger Context

### The Zero-Point Singularity
At Gameweek 1 of any new FPL campaign, all live player tables report Total Points ($\text{TP} = 0$). In the standard Chimera feature engineering pipeline:
1. **Prophetic Points Collapse:** $\text{PP} = \text{TP} \times \text{Captaincy\_Coef} = 0 \times 1.25 = 0.0$.
2. **Form Factor Collapse:** Lookback $\text{GW} - 6 \le 0$ falls back to $\text{Form\_Factor} = \text{TP} = 0.0$.
3. **Objective Function Degeneracy:**
   $$\text{Final\_Score} = \frac{\text{PP} + \text{SPP} + (\text{Form\_Factor} \times 0.5)}{\text{Effective\_FDR\_Horizon\_5GW}} = \frac{\text{SPP}}{\text{Effective\_FDR\_Horizon\_5GW}}$$
   Without intervention, the solver degenerates into selecting players purely based on Set-Piece Potency ($\text{SPP}$) and easy fixtures, treating Erling Haaland or Mohamed Salah identically to £4.0m non-playing assets.

### The Prior-Season Baseline (Bayesian Decay Schedule)
To establish true player quality prior to in-season sample accumulation, the engine incorporates historical statistics from the previous campaign (e.g., $2025/26$). As the season progresses through GW1 to GW6, reliance on the prior season decays linearly into pure current-season performance:

$$\alpha_t = \max\left(0, 1 - \frac{t - 1}{5}\right), \quad t \in \{1, 2, 3, 4, 5, 6\}$$

$$\text{Effective\_Metric}(i, t) = (1 - \alpha_t) \cdot \text{Current\_Metric}(i, t) + \alpha_t \cdot \text{Prior\_Baseline}(i)$$

- **GW1 ($\alpha_1 = 1.0$):** 100% Prior Season baseline (normalized against 2026/27 starting prices).
- **GW2 ($\alpha_2 = 0.8$):** 80% Prior Season / 20% GW1 performance.
- **GW3 ($\alpha_3 = 0.6$):** 60% Prior Season / 40% In-Season actuals.
- **GW4 ($\alpha_4 = 0.4$):** 40% Prior Season / 60% In-Season actuals.
- **GW5 ($\alpha_5 = 0.2$):** 20% Prior Season / 80% In-Season actuals.
- **GW6+ ($\alpha_6 = 0.0$):** 100% In-Season sample ($\ge 5\text{--}6$ gameweeks of live data).

### Ingestion Heterogeneity (Prior Season HTML)
End-of-season historical dumps differ structurally from weekly in-season position tables:
- **No Positional Partitioning:** Contains all 600+ players in a single unified table rather than separate `gkp.html`, `def.html`, etc.
- **Header Divergence:** Columns represent full-season aggregates (`Total Points`, `Minutes`, `Goals`, `Assists`, `Clean Sheets`, `Bonus`, `ICT/xGI`, `Selected %`) rather than weekly form.
- **Player Transfers & Promoted Clubs:** Requires fuzzy name and team aliasing to align newly transferred players with their 2026/27 clubs.

### Greenfield Treasury State
Unlike mid-season optimization which enforces purchase price lock-in and the 50% selling profit tax via `squad.csv`, GW1 operates with an unconstrained £100.0m bank and zero transfer transaction costs.

---

## 3. Dynamic Chaos vs. Typed Mathematical Truth

| Feature / Dimension | Naive Dynamic Chaos (❌) | Typed Mathematical Truth (✅) |
| :--- | :--- | :--- |
| **GW1 Points Evaluation** | Calculates $TP=0 \implies PP=0$, selecting squad purely on set pieces and FDR. | Blends prior-season baseline via decaying Bayesian shrinkage parameter $\alpha_t \in [0, 1]$. |
| **Historical Data Ingestion** | Ad-hoc manual copy-pasting into in-season CSV templates with mismatched columns. | Dedicated `process_prior_season_html` parser normalizing full-year aggregates into structured priors. |
| **GW1 Treasury Model** | Errors on missing `squad.csv` or forces artificial sell-price calculations. | Greenfield mode: Flat £100.0m budget constraint with 0 transfer penalty variables. |
| **Seasonal Rollover State** | Leaves 30+ legacy gameweek directories in root, breaking numeric `get_latest_gw()` sorting. | Surgical archival into `archive/YYYY-YY/` via deterministic `bamf archive-season <tag>` command. |
| **Club Entity Realities** | Crashes on newly promoted teams due to stale hardcoded `TEAM_NAME_TO_TLA` dictionary. | Automated reality audit verifying all 20 active Premier League clubs and set-piece takers. |

---

## 4. The Pattern (Anti-Pattern vs. Idiomatic Implementation)

### ❌ WRONG: Naive Cold-Start Fallback
```python
# CRITICAL DEFECT: At GW1, players['TP'] is 0. Form_Factor and PP collapse to 0.0!
if past_gw <= 0:
    players["Form_Factor"] = players["TP"]  # 0.0
players["PP"] = players["TP"] * players["Captaincy_Coef"]  # 0.0
players["Final_Score"] = (players["PP"] + players["SPP"]) / players["FDR"]
# Result: Erling Haaland Final_Score = 0.0 (unless penalty taker)
```

### ✅ RIGHT: Decaying Historical Prior Architecture
```python
def calculate_prophetic_score_with_prior(
    current_df: pd.DataFrame,
    prior_baseline_df: pd.DataFrame,
    gameweek_num: int,
    form_lookback: int = 5,
) -> pd.DataFrame:
    """
    Computes effective player metric using linear Bayesian decay from prior season.
    """
    # Calculate decay weight alpha_t: 1.0 at GW1 down to 0.0 at GW6
    alpha = max(0.0, 1.0 - (gameweek_num - 1) / float(form_lookback))
    
    merged = pd.merge(
        current_df,
        prior_baseline_df[["Surname", "Team", "Prior_PPM", "Prior_TP"]],
        on=["Surname", "Team"],
        how="left",
    )
    # Fill newcomers / promoted assets with position-average prior
    merged["Prior_TP"] = merged["Prior_TP"].fillna(merged.groupby("Position")["Prior_TP"].transform("median"))
    
    # Calculate synthetic baseline points scaled to 2026/27 price
    merged["Baseline_TP"] = merged["Prior_TP"]
    
    if alpha > 0.0:
        merged["Effective_TP"] = (1.0 - alpha) * merged["TP"] + alpha * merged["Baseline_TP"]
    else:
        merged["Effective_TP"] = merged["TP"]
        
    merged["PP"] = (merged["Effective_TP"] * merged["Captaincy_Coef"]).round(2)
    return merged
```

---

## 5. Verification Checklist for Season Transitions

1. **Tag & Archive:** Run `git tag -a season-XXXX-YY-final` and execute `bamf archive-season XXXX-YY`.
2. **Team Realities Audit:** Verify all 20 clubs in `TEAM_NAME_TO_TLA` across `grand_synthesis.py` and `audit_realities.py`.
3. **Set-Piece Database Audit:** Update penalty, free-kick, and corner takers in `set_pieces.csv`.
4. **Prior Season Ingestion:** Ingest prior season historical dump to establish `Baseline_TP` for GW1–GW5 optimization.
5. **Greenfield GW1 Optimization:** Ensure `bamf finalize gw1` runs with flat £100.0m bank and unconstrained squad selection.
