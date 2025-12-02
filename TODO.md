# PROJECT: BAMF DOMINATOR - STRATEGIC BLUEPRINT (v5.0)

## MISSION STATEMENT

To systematically dismantle and dominate the Fantasy Premier League simulation by transforming raw, chaotic data into a decisive strategic advantage. We will build an analytical and predictive engine—the Chimera—to forge the optimal squad week after week, guided by logic, mathematics, and a touch of madness. This is our shared voyage `(⇌)`, and this document is our map.

---

## ✅ PHASE 8: THE TEMPORAL LENS (FUTURE DISCOUNTING) (Completed)

The Chimera currently views all upcoming fixtures with equal importance. We will now grant it a more nuanced understanding of time, teaching it that immediate challenges are more critical than distant ones. We will implement a "future discounting" model for fixture difficulty, making our `Effective_FDR_Horizon_5GW` metric smarter and more responsive to the immediate schedule.

### 8.1: Forge the Temporal Weights `(⊕)`

-   `[x]` **Define the Discounting Model:** We will use a weighted average for the 5-gameweek fixture horizon, where closer matches have a higher weight.
-   `[x]` **Update `config.yaml`:** Add a new `temporal_discounting` section to `config.yaml`. This will contain a `fixture_weights` list (e.g., `[1.0, 0.8, 0.6, 0.4, 0.2]`) that defines the weight for each of the next 5 gameweeks.

### 8.2: Evolve the Grand Synthesis `(⇌)`

-   `[x]` **Refactor `grand_synthesis.py`:** This is the heart of the operation.
    -   The script must load the new `fixture_weights` from `config.yaml`.
    -   The `fdr_horizon` calculation must be upgraded. Instead of a simple `.mean()`, it will now calculate a weighted average for both `FDR_A_Horizon_5GW` and `FDR_D_Horizon_5GW` based on the new weights. This will likely involve grouping fixtures by team and then applying the weighted calculation to each group.

### 8.3: Full System Verification

-   `[x]` **Run the Gauntlet:** Execute the full `bamf run-gauntlet gw12` command to see the effect of the new temporal logic.
-   `[x]` **Analyze the Impact:** Compare the new `OMNISCIENT.csv` and `squad_prophecy.md` with the previous versions. Has the squad selection changed? Are players with tough upcoming fixtures now penalized more heavily? This will verify that our new temporal lens is focusing the Chimera's gaze correctly.

---

## ✅ PHASE 9: THE SCRIBE'S AUTOMATION & TEMPORAL VERIFICATION (Completed)

We have refined the Chimera's understanding of the future and equipped it with a new data ingestion tool. This phase focuses on automating data input and rigorously testing our temporal discounting logic.

### 9.1: Automate HTML Fixture Ingestion `(⊕)`

-   `[x]` **Generic HTML Parser:** We have already forged `src/fpl_dominator/process_fixtures_html.py` which can now process any gameweek's HTML fixture files into a CSV.
-   `[x]` **Integrate into Workflow:** Integrate `process_fixtures_html.py` as a new command within `bamf.py` to streamline fixture data processing.

### 9.2: Temporal Discounting Logic Verification `(⇌)`

-   `[⌑]` **Create Synthetic Data Test:** Forge a new script (`src/fpl_dominator/verify_temporal_logic.py`) to create a synthetic `fixtures_df` with deliberately varied fixture difficulties (e.g., Team A: Hard-Easy-Easy, Team B: Easy-Easy-Hard).
-   `[⌑]` **Apply Weighted Average:** Apply the `grand_synthesis.py`'s weighted average logic to this synthetic data.
-   `[⌑]` **Verify Ranking Change:** Assert that the calculated `Effective_FDR_Horizon_5GW` values for the synthetic teams correctly reflect the temporal discounting, leading to a change in their relative rankings. This will definitively prove the integrity of our Temporal Lens.

---

### NDH GLYPH KEY

- `⊕ (forge)`: The act of creation, building, synthesis.
- `⇌ (barb)`: Our shared forward voyage of discovery and collaboration.
- `⁂ (fungi)`: Mycelial, distributed, underlying network/intelligence.
- `π (pie)`: The Carbon Pirate (human) element; our strategic insight.
- `⌑ (mole)`: A strategic retreat or putting a task on the back-burner.
