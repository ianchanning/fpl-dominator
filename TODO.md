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

## 🔴 PHASE 1: THE CHIMERA FORGE (Current Objective)

### 1.1: Core Optimizer v1 (Proof of Concept - "The Naive God")

- `[x]` **Create `chimera_forge.py` script.**
- `[x]` **Implement a baseline optimizer** to maximize `TP` for a 15-man squad.
- `[x]` **BREADCRUMB:** The v1 Chimera successfully proved the core logic but revealed a critical flaw: it created a team of 15 "starters" with no concept of a bench. This "Naive God" was a necessary but insufficient step, prompting an immediate evolution.

### 1.2: Strategic Core Optimizer v2 (The "Split-Brain")

- `[x]` **Create `chimera_forge_v2_strategic.py` script.**
- `[x]` **Evolve the optimizer** with a dual-layer logic:
  - Introduce separate decision variables for `in_squad` and `is_starter`.
  - Change the objective function to **maximize the `TP` of the 11-man starting XI only.**
  - Add constraints for a valid starting formation.
- `[ ]` **Execute and analyze the output** of the v2 Chimera. This will be our new, intelligent baseline for all future strategies.

### 1.3: Implement Strategic Scenarios

- `[ ]` **Refactor the v2 optimizer** into a function that can accept lists of players to _force into_ or _exclude from_ the squad.
- `[ ]` **Simulate "The Haaland Hammer":** Run the v2 optimizer with Haaland pre-selected.
- `[ ]` **Simulate "The Salah God-Tier":** Run the v2 optimizer with Salah pre-selected.
- `[ ]` **Simulate "The Gods of Chaos":** Run the v2 optimizer with _both_ Haaland and Salah pre-selected.
- `[ ]` **Simulate "The Balanced Brigade":** Run the v2 optimizer while explicitly _excluding_ all players above a certain price threshold (e.g., > £10.0m).

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
