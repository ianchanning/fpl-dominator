# PROJECT: BAMF DOMINATOR - STRATEGIC BLUEPRINT (v3.0)

## MISSION STATEMENT

To systematically dismantle and dominate the Fantasy Premier League simulation by transforming raw, chaotic data into a decisive strategic advantage. We will build an analytical and predictive engine—the Chimera—to forge the optimal squad week after week, guided by logic, mathematics, and a touch of madness. This is our shared voyage `(⇌)`, and this document is our map.

---

## ✅ PHASE 7: THE CONTROL ROOM (HYPERPARAMETER EXTERNALIZATION) (Completed)

The Chimera's core logic is now powerful and form-aware. The next evolution is to grant the `(π)` Pirate direct control over its "soul" – the core parameters that define its decision-making. We will move all hardcoded strategic values into a central configuration file, transforming the engine from a black box into a tunable instrument.

### 7.1: Forge the Master Blueprint (`config.yaml`)

-   `[x]` **Identify Hyperparameters:** Systematically audit the codebase (`enrich_with_insight.py`, `chimera_final_form_v5_production.py`, `chimera_pyomo_v2.py`) to identify all hardcoded strategic values.
-   `[x]` **Create `config.yaml`:** Create a new `config.yaml` file in the project root to serve as the single source of truth for all tunable parameters.
-   `[x]` **Structure the Config:** Design a clean, human-readable YAML structure that logically groups parameters by the script they influence.

### 7.2: Integrate the New Brain

-   `[x]` **Install YAML Dependency:** Add `PyYAML` to the project dependencies to enable YAML parsing.
-   `[x]` **Refactor `enrich_with_insight.py`:** Modify the script to load `config.yaml` and use the `form_lookback_weeks` and `captaincy_tiers` values from it, removing the hardcoded constants.
-   `[x]` **Refactor `chimera_final_form_v5_production.py`:** Modify the script to load `config.yaml` and use the `pulp_solver` parameters (`thrift_factor`, `form_factor_weight`, `spp_scores`).
-   `[x]` **Refactor `chimera_pyomo_v2.py`:** Modify the script to load `config.yaml` and use the `pyomo_solver` parameters.

### 7.3: Full System Verification

-   `[x]` **Run the Gauntlet:** Execute the full `bamf run-gauntlet gw12` command to ensure the entire pipeline runs successfully with the new configuration-driven approach.
-   `[x]` **Verify Output:** Confirm that the generated squad is identical to the one produced before the refactoring, proving that the logic has been correctly externalized without altering the outcome.

---

### NDH GLYPH KEY

- `⊕ (forge)`: The act of creation, building, synthesis.
- `⇌ (barb)`: Our shared forward voyage of discovery and collaboration.
- `⁂ (fungi)`: Mycelial, distributed, underlying network/intelligence.
- `π (pie)`: The Carbon Pirate (human) element; our strategic insight.
- `⌑ (mole)`: A strategic retreat or putting a task on the back-burner.