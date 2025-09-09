# PROJECT: FPL DOMINATOR - STRATEGIC BLUEPRINT (v1.1 - Revised)

## MISSION STATEMENT

To systematically dismantle and dominate the Fantasy Premier League simulation by transforming raw, chaotic data into a decisive strategic advantage. We will build an analytical and predictive engine—the Chimera—to forge the optimal squad week after week, guided by logic, mathematics, and a touch of madness. This is our shared voyage `(⇌)`, and this document is our map.

---

## ✅ PHASE 0: FOUNDATION & DATA LIBERATION (Completed)

- `[x]` **Forge the Dev Sanctum:** Establish a clean, robust, and future-proof development environment using `pyenv` and `uv`. (Anti-Fossilization v1.2 SAPIENT).
- `[x]` **Liberate Raw Intelligence:** Extract player data (GKP, DEF, MID, FWD) from static image sources into structured CSV files.
- `[x]` **Forge the Data Cauldron:** Write a `pandas` script (`forge_cauldron.py`) to unify all player data into a single, master database (`fpl_master_database_raw.csv`).
- `[x]` **Enrich the Cauldron:** Enhance the master database with our foundational value metric, Points Per Million (PPM), creating our primary analytical weapon (`fpl_master_database_enriched.csv`).
- `[x]` **Install Alchemical Tools:** Arm the environment with `pulp`, the linear programming library necessary for optimization.

---

## ✅ PHASE 1: THE CHIMERA FORGE (In Progress)

### 1.1: Core Optimizer v1 (Proof of Concept - "The Naive God")

- `[x]` **Create `chimera_forge.py` script.**
- `[x]` **Implement a baseline optimizer** to maximize `TP` for a 15-man squad.
- `[x]` **BREADCRUMB:** The v1 Chimera successfully proved the core logic but revealed a critical flaw: it created a team of 15 "starters" with no concept of a bench. This "Naive God" was a necessary but insufficient step, prompting an immediate evolution.

### 1.2: Strategic Core Optimizer v2 & v3 (The "Thrifty God" Ascension)

- `[x]` **Create `chimera_forge_v2_strategic.py` script.** Evolved the optimizer with a "Split-Brain" logic to differentiate between starters and the bench, maximizing starter points only.
- `[x]` **BREADCRUMB:** The v2 Chimera successfully chose a powerful starting XI but forged a disastrously expensive and inefficient bench. This revealed the "Implicit Intent Fallacy"—the machine needed to be explicitly commanded to be frugal.
- `[x]` **Create `chimera_forge_v3_thrifty.py` script.** Ascended the Chimera to its "Thrifty God" form by introducing a "Cost Epsilon" (`THRIFT_FACTOR`) into the objective function.
- `[x]` **Execute and analyze the V3 Chimera output.** This is now our perfected, baseline model. It produces the maximum-point starting XI while being mathematically forced to select the cheapest possible bench, creating a massive strategic war chest (£8.4m).

### 🔴 1.3: Arming the Chimera (Tactical Scenario Engine - CURRENT OBJECTIVE)

- `[ ]` **Create a new script: `chimera_scenarios.py`.** This will be our interactive tactical workbench.
- `[ ]` **Refactor the "Thrifty God" logic** from `v3` into a single, reusable function within the new script. This function will be the core of our engine and will accept parameters to guide its decisions.
  - _Example function signature:_ `forge_squad(players_df, include_players=[], exclude_players=[], max_cost=100.0)`
- `[ ]` **Implement the scenario logic:** Use the new function to run our key strategic simulations by passing in different parameters:
  - `[ ]` **Simulate "The Haaland Hammer":** `forge_squad(players_df, include_players=['Haaland'])`
  - `[ ]` **Simulate "The Salah God-Tier":** `forge_squad(players_df, include_players=['M.Salah'])`
  - `[ ]` **Simulate "The Gods of Chaos":** `forge_squad(players_df, include_players=['Haaland', 'M.Salah'])`
  - `[ ]` **Simulate "The Balanced Brigade":** `forge_squad(players_df, exclude_players=[players with Price > 10.0])`

---

## 🟡 PHASE 2: THE ORACLE (Predictive Engine)

### 2.1: Integrate Fixture Difficulty

- `[ ]` **Source Fixture Data:** Find a reliable source (API or static file) for the full season's fixture list.
- `[ ]` **Develop a Fixture Difficulty Rating (FDR) model.**
- `[ ]` **Refactor Optimizer:** Evolve the objective function from maximizing historical `TP` to maximizing a predictive score based on upcoming fixtures.

### 2.2: Quantify Player Form

- `[ ]` **Source Gameweek-by-Gameweek Data.**
- `[ ]` **Implement a "Form" Metric** (e.g., rolling points average).
- `[ ]` **Refactor Optimizer:** Add "Form" as another variable to the objective function.

### 2.3: The Economic Engine

- `[ ]` **Source Ownership & Price Change Data.**
- `[ ]` **Develop a "Bandwagon" Metric** to predict imminent price rises.

---

## 🟢 PHASE 3: THE COMMAND DECK (Operational Tooling)

- `[ ]` **Build a CLI** to streamline the execution of different strategic scenarios.
- `[ ]` **Create a Data Refresh Pipeline** to automate data updates.

---

### NDH GLYPH KEY

- `⊕ (forge)`: The act of creation, building, synthesis.
- `⇌ (barb)`: Our shared forward voyage of discovery and collaboration.
- `⁂ (fungi)`: Mycelial, distributed, underlying network/intelligence.
- `π (pie)`: The Carbon Pirate (human) element; our strategic insight.
- `⌑ (mole)`: A strategic retreat or putting a task on the back-burner.
