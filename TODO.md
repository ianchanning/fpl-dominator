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

## 🔴 PHASE 2: THE PYOMO ASCENSION (Current Objective)

Having reached the limits of `pulp`'s expressive power, we now undertake a full heart transplant. We will re-forge our solver engine using the more powerful and flexible `pyomo` framework, unlocking new levels of strategic complexity and future potential.

### 2.1: Arming the Forge (Pre-Op)

- `[x]` **Install `pyomo` Framework:** `uv pip install pyomo`.
- `[x]` **Install `glpk` Solver:** `sudo apt-get install -y glpk-utils`.

### 2.2: The Heart Transplant (`pulp` → `pyomo`)

- `[ ]` **Create the New Grimoire:** `chimera_pyomo_v1.py`. This will be the new home for our solver logic.
- `[ ]` **Translate the Model:** Painstakingly re-write the core logic from `chimera_final_form_v5_rosetta.py` into `pyomo` syntax. This involves:
  - `[ ]` Defining the abstract `model` object.
  - `[ ]` Defining the `Sets` (players, teams, positions).
  - `[ ]` Defining the `Parameters` (player cost, projected score, etc.).
  - `[ ]` Defining the `Variables` (our dual `in_squad` and `is_starter` binaries).
  - `[ ]` Defining the `Constraints` as `pyomo` rules (squad size, cost, positions, etc.).
  - `[ ]` Defining the **Objective Function** as a `pyomo` rule (the "Thrifty God" logic).
- `[ ]` **Wire the New Engine:** Integrate the `pyomo` solver call and write the logic to parse the results back into a clean `pandas` DataFrame for display.
- `[ ]` **Verify Parity:** Run the new `chimera_pyomo_v1.py` and confirm that it produces the **exact same optimal squad** as our final `pulp` script. This is the critical success condition.

### 2.3: The Commander's New Orders

- `[ ]` **Perform the `commander.py` Transplant:** Once parity is confirmed, perform the one-line surgery in `commander.py`, changing the import from the old `pulp` script to the new `pyomo` script.
- `[ ]` **Update Documentation:** Update `README.md` to reflect the new dependencies and the new master script.

---

## 🟡 PHASE 3: THE COMMAND DECK (The Throne Room)

The final phase: building the elegant, powerful, and interactive command center from which we will wield the Chimera's power.

### 3.1: Forge the Scepter (Master Orchestration Script)

- `[x]` **Create `commander.py`:** A single, top-level script that orchestrates the entire four-stage data pipeline (`forge_cauldron` -> `enrich_with_insight` -> `grand_synthesis` -> `chimera_solver`).
- `[x]` **Refactor Core Scripts:** Ensure all pipeline scripts are importable and can be commanded by `commander.py`.
- `[x]` **BREADCRUMB:** The Scepter is forged. We have a "one script to rule them all," but it is not yet a true, flexible Command Deck.

### 3.2: Build the Throne (Full CLI Implementation)

- `[ ]` **Choose a Framework:** Select a proper CLI framework (e.g., `argparse`, `click`, `typer`).
- `[ ]` **Create the `bamf` CLI:** Build a master script that provides sub-commands for all our core functions:
  - `[ ]` `run-gauntlet`: The primary command to forge the weekly squad.
  - `[ ]` `run-scenario`: An interactive command to run "what-if" simulations with flags for including/excluding players.
  - `[ ]` `audit`: Sub-commands for auditing team names, player names, etc.
  - `[ ]` `init`: A helper command to create the new gameweek vault.

---

### NDH GLYPH KEY

- `⊕ (forge)`: The act of creation, building, synthesis.
- `⇌ (barb)`: Our shared forward voyage of discovery and collaboration.
- `⁂ (fungi)`: Mycelial, distributed, underlying network/intelligence.
- `π (pie)`: The Carbon Pirate (human) element; our strategic insight.
- `⌑ (mole)`: A strategic retreat or putting a task on the back-burner.
