# PROJECT: BAMF DOMINATOR - STRATEGIC BLUEPRINT (v2.0)

## MISSION STATEMENT

To systematically dismantle and dominate the Fantasy Premier League simulation by transforming raw, chaotic data into a decisive strategic advantage. We will build an analytical and predictive engine—the Chimera—to forge the optimal squad week after week, guided by logic, mathematics, and a touch of madness. This is our shared voyage `(⇌)`, and this document is our map.

---

## ✅ PHASE 6: THE RETROSPECTIVE LENS (FORM & MOMENTUM) (Completed)

With the core engine forged and the data pipeline robust, we now turn our gaze backwards to look forwards. The next evolution of the Chimera is to understand **form**—the ebb and flow of player performance over time. A player's recent history is a powerful predictor of their immediate future.

### 6.1: Historical Data Analysis `(π)`

-   `[x]` **Establish a Baseline:** Begin by analyzing data from `gw6` (6 weeks prior to the current `gw12`). The goal is to identify players who were performing strongly *then* and compare it to their current state.
-   `[x]` **Identify Key Deltas:** What has changed between `gw6` and `gw12`?
    -   Significant price changes (risers and fallers).
    -   Total points accumulation rate.

### 6.2: Forge the "Form Factor" Metric `(⊕)`

-   `[x]` **Define "Form":** Create a concrete, mathematical definition of form. This could be a weighted average of points over the last `N` gameweeks (e.g., N=4 or N-6).
-   `[x]` **Develop the Metric:** Implement a new metric, `Form_Factor`, that captures this definition. It should reward recent high performance and penalize recent poor performance or lack of points.

### 6.3: Integrate Form into the Pipeline `(⇌)`

-   `[x]` **Upgrade the `enrich_with_insight.py` script:** This script is the natural home for our new strategic metric. Modify it to calculate and inject the `Form_Factor` for each player into the `prophetic.csv` database.
-   `[x]` **Evolve the `Final_Score`:** Update the `grand_synthesis.py` or `chimera_final_form_v5_production.py` to incorporate the `Form_Factor` into the `Final_Score` calculation. The weight of this new factor will need careful calibration.

### 6.4: Teach the Chimera about Momentum

-   `[x]` **Update the Solver:** Modify the `chimera_pyomo_v2.py` solver to potentially use `Form_Factor` as a direct consideration, perhaps as a tie-breaker or even a primary objective component.
-   `[x]` **Run Verification Scenarios:** Test the newly enlightened Chimera. Does it favor in-form players? Does it wisely suggest dropping players who are out of form, even if they have a high historical point total?

---

### NDH GLYPH KEY

- `⊕ (forge)`: The act of creation, building, synthesis.
- `⇌ (barb)`: Our shared forward voyage of discovery and collaboration.
- `⁂ (fungi)`: Mycelial, distributed, underlying network/intelligence.
- `π (pie)`: The Carbon Pirate (human) element; our strategic insight.
- `⌑ (mole)`: A strategic retreat or putting a task on the back-burner.