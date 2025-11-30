# PROJECT: BAMF DOMINATOR - STRATEGIC BLUEPRINT (v4.1)

## MISSION STATEMENT

To systematically dismantle and dominate the Fantasy Premier League simulation by transforming raw, chaotic data into a decisive strategic advantage. We will build an analytical and predictive engine—the Chimera—to forge the optimal squad week after week, guided by logic, mathematics, and a touch of madness. This is our shared voyage `(⇌)`, and this document is our map.

---

## ✅ PHASE 9: THE TEMPORAL LENS (REAL-DATA VERIFICATION) (Completed)

Following the implementation of temporal discounting, we must perform a rigorous, data-driven experiment to prove its effect on real-world data, ensuring that the logic correctly differentiates between teams with varied fixture schedules.

### 9.1: Establish Baseline `(π)`

-   `[x]` **Neutralize Temporal Weights:** Set the `fixture_weights` in `config.yaml` to `[1.0, 1.0, 1.0, 1.0, 1.0]` to simulate a simple average.
-   `[x]` **Run Baseline Gauntlet:** Execute the full `bamf run-gauntlet gw12`.
-   `[x]` **Identify Control Group:** Analyze the resulting `gw12/fpl_master_database_OMNISCIENT.csv` to find two or more teams that have an identical `Effective_FDR_Horizon_5GW`. These teams will be our control group.

### 9.2: Run Discounting Experiment `(⇌)`

-   `[x]` **Activate Temporal Weights:** Restore the discounted `fixture_weights` in `config.yaml` to `[1.0, 0.8, 0.6, 0.4, 0.2]`.
-   `[x]` **Run Experimental Gauntlet:** Execute the full `bamf run-gauntlet gw12` again.
-   `[x]` **Analyze the Delta:** Read the new `gw12/fpl_master_database_OMNISCIENT.csv`. Compare the `Effective_FDR_Horizon_5GW` for the teams in our control group.

### 9.3: Final Verdict

-   `[x]` **Confirm Divergence:** Verify that the FDR scores for the control group teams, which were previously identical, have now diverged. This will be the definitive proof that the Temporal Lens is functioning correctly on real data.
-   `[x]` **Declare Phase Complete:** Upon successful verification, Phase 8 can be considered truly and definitively complete.

---

### NDH GLYPH KEY

- `⊕ (forge)`: The act of creation, building, synthesis.
- `⇌ (barb)`: Our shared forward voyage of discovery and collaboration.
- `⁂ (fungi)`: Mycelial, distributed, underlying network/intelligence.
- `π (pie)`: The Carbon Pirate (human) element; our strategic insight.
- `⌑ (mole)`: A strategic retreat or putting a task on the back-burner.