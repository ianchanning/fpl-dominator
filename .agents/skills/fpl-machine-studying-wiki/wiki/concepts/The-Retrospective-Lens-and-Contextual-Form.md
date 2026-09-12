# The Retrospective Lens & Contextual Form (RFC-011)

## 1. The Sovereign Law
Weight historical player points by normalized opposition fixture difficulty ($\text{FDR}_{\text{past}} / 1000.0$) using positional bifurcation: raw form is a misleading lagging indicator that inflates soft-schedule stat-padders and penalizes suppressed elites.

---

## 2. The Formulation & Trigger Context

### The Stat-Padding Fallacy
In naive FPL optimization algorithms, player form is formulated as a blind difference or rolling sum of points:
$$\text{Raw\_Form}_i = \text{TP}_{i, t} - \text{TP}_{i, t-L}$$

This treats all points identically, creating severe strategic vulnerabilities:
1. **Chasing Ghost Form:** A defender or forward bagging points against bottom-tier relegation fodder ($\text{FDR} \approx 1000$) is rated higher than an elite asset battling top-four defensive walls ($\text{FDR} \approx 1350$). The solver buys the stat-padder right before their fixture difficulty turns brutal.
2. **Discarding Suppressed Elites:** Elite assets enduring a difficult fixture run are penalized for low raw totals and dropped from the squad, right before their schedule softens.
3. **The 38-Game Annualized Gremlin:** When blending Bayesian priors in early-season transitions, subtracting historical raw points from 38-game annualized points introduces fatal scale distortion.

---

## 3. Dynamic Chaos vs. Typed Mathematical Truth

| Dimension | Naive Raw Form (❌) | Retrospective Lens Truth (✅) |
| :--- | :--- | :--- |
| **Opposition Context** | Blind; 10 pts vs Southampton = 10 pts vs Arsenal. | **Difficulty-Weighted:** 10 pts scaled by $\text{FDR}_{\text{past}} / 1000.0$. |
| **Positional Bifurcation** | None; treats attacker and defender difficulty identically. | **Bifurcated:** Midfielders/Forwards evaluate against $\text{FDR}_A$, Defenders/Goalkeepers against $\text{FDR}_D$. |
| **Mathematical Equation** | $\text{Form} = \sum \Delta \text{Pts}_g$ | $\text{Adjusted\_Form} = \sum_{g} \left(\Delta \text{Pts}_g \times \frac{\text{FDR}_{g}}{1000.0}\right)$. |
| **Efficiency Metric** | None; only tracks absolute points. | $\text{Efficiency} = \frac{\sum \Delta \text{Pts}}{\sum \text{xPts}(\text{FDR})}$; tracks performance relative to schedule. |
| **Scenario Forge Audit** | Cannot isolate schedule noise from genuine form. | Binary audit (`bamf forge --compare-form`) surfaces **Form Frauds** and **Sleepers**. |

---

## 4. The Pattern (❌ WRONG vs. ✅ RIGHT)

### ❌ WRONG: Context-Blind Form Subtraction
```python
# CRITICAL FLAW: Blind subtraction ignores fixture difficulty and mixes annualized TP with raw TP
if current_gw >= 6:
    players["Form_Factor"] = players["TP"] - df_past["TP"]
```

### ✅ RIGHT: Pure Retrospective Lens Extraction (`retrospective_lens.py`)
```python
def calculate_retrospective_form(
    players_df: pd.DataFrame,
    current_gw: int,
    lookback_weeks: int = 2,
) -> pd.DataFrame:
    """Calculates fixture-adjusted form and efficiency using historical vaults."""
    fdr_map = extract_historical_fixture_fdr(current_gw, lookback_weeks)
    points_delta_map = extract_historical_player_points(current_gw, lookback_weeks)

    adjusted_forms = []
    efficiencies = []

    for _, row in players_df.iterrows():
        surname = str(row["Surname"])
        team_tla = TEAM_NAME_TO_TLA.get(row["Team"])
        pos = row["Position"]
        deltas = points_delta_map.get((surname, row["Team"]), {})

        total_adjusted = 0.0
        total_raw = 0.0
        total_exp = 0.0

        for gw, pts in deltas.items():
            fdr_dict = fdr_map.get((team_tla, gw), {})
            fdr = fdr_dict["FDR_D"] if pos in ["GKP", "DEF"] else fdr_dict["FDR_A"]
            total_raw += pts
            total_adjusted += pts * (fdr / 1000.0)

            base_exp = 3.5 if pos in ["GKP", "DEF"] else 4.5
            total_exp += base_exp * (1150.0 / max(800.0, fdr))

        adjusted_forms.append(round(total_adjusted, 2))
        efficiencies.append(round(total_raw / max(0.5, total_exp), 2))

    players_df["Adjusted_Form"] = adjusted_forms
    players_df["Form_Efficiency"] = efficiencies
    return players_df
```
