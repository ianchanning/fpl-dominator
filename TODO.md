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

- `[x]` **BREADCRUMB:** Successfully proved the core optimization logic but revealed the tactical necessity of a bench.

### 1.2: Strategic Core Optimizer v2 & v3 (The "Thrifty God" Ascension)

- `[x]` **BREADCRUMB:** Successfully evolved the Chimera to understand the Starter/Bench duality and to be ruthlessly cost-efficient, forging our perfected baseline model.

### 1.3: Arming the Chimera (Tactical Scenario Engine)

- `[x]` **Create `chimera_scenarios.py` script.**
- `[x]` **Refactor the "Thrifty God" logic** into a reusable, parameter-driven function.
- `[x]` **Execute and analyze all core strategic scenarios.**
- `[x]` **BREADCRUMB:** The simulations were a monumental success but revealed the Chimera's final, critical flaw: "Captaincy Blindness." It optimizes based on pure historical points (`TP`) and has no concept of a player's explosive ceiling or their value as a weekly captaincy choice. This was proven when it benched M.Salah.

### 🔴 1.4: Granting Sight (The Captaincy Coefficient - CURRENT OBJECTIVE)

- `[ ]` **Create a new script: `enrich_with_insight.py`.** This script will be used to inject our `(π)` pirate's strategic knowledge into the raw data.
- `[ ]` **Define the "Captaincy Coefficient":**
  - In the new script, load the `fpl_master_database_enriched.csv`.
  - Create a new column called `Captaincy_Coef`.
  - Assign coefficients based on our strategic assessment:
    - **Tier 1 (Gods):** Haaland, M.Salah -> Coef `1.5`
    - **Tier 2 (Demigods):** Other reliable, high-ceiling assets (e.g., João Pedro, Ekitiké, Enzo) -> Coef `1.2`
    - **Tier 3 (Mortals):** Everyone else -> Coef `1.0`
- `[ ]` **Create the `Prophetic_Points` Metric:**
  - Create a new column, `PP` (Prophetic Points), calculated as `TP * Captaincy_Coef`.
- `[ ]` **Save a new, final database:** `fpl_master_database_prophetic.csv`.
- `[ ]` **Create `chimera_prophet.py`:**
  - Copy the `chimera_scenarios.py` script to a new file.
  - Modify it to load the new `prophetic` database.
  - Change the objective function to maximize the sum of `PP` instead of `TP`.
- `[ ]` **Run the "Salah God-Tier" scenario** with the new Prophet Chimera and verify that it now correctly places Salah in the starting XI.

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
