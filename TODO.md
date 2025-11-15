# PROJECT: BAMF DOMINATOR - STRATEGIC BLUEPRINT (v1.6)

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

## ✅ PHASE 1: THE PULP-POWERED CHIMERA (Completed & Archived)

### 1.1: Core Optimizer v1 (Proof of Concept - "The Naive God")

- `[x]` **BREADCRUMB:** Successfully proved the core optimization logic but revealed the tactical necessity of a bench.

### 1.2: Strategic Core Optimizer v2 & v3 (The "Thrifty God" Ascension)

- `[x]` **BREADCRUMB:** Successfully evolved the Chimera to understand the Starter/Bench duality and to be ruthlessly cost-efficient, forging our perfected baseline model.

### 1.3: Arming the Chimera (Tactical Scenario Engine)

- `[x]` **Create `chimera_scenarios.py` script.**
- `[x]` **Refactor the "Thrifty God" logic** into a reusable, parameter-driven function.
- `[x]` **Execute and analyze all core strategic scenarios.**
- `[x]` **BREADCRUMB:** The simulations were a monumental success but revealed the Chimera's final, critical flaw: "Captaincy Blindness." It optimizes based on pure historical points (`TP`) and has no concept of a player's explosive ceiling or their value as a weekly captaincy choice. This was proven when it benched M.Salah.

### 🔴 1.4: Granting Sight (The Captaincy Coefficient)

- `[x]` **Create a new script: `enrich_with_insight.py`.** This script will be used to inject our `(π)` pirate's strategic knowledge into the raw data.
- `[x]` **Define the "Captaincy Coefficient":**
  - In the new script, load the `fpl_master_database_enriched.csv`.
  - Create a new column called `Captaincy_Coef`.
  - Assign coefficients based on our strategic assessment:
    - **Tier 1 (Gods):** Haaland, M.Salah -> Coef `1.5`
    - **Tier 2 (Demigods):** Other reliable, high-ceiling assets (e.g., João Pedro, Ekitiké, Enzo) -> Coef `1.2`
    - **Tier 3 (Mortals):** Everyone else -> Coef `1.0`
- `[x]` **Create the `Prophetic_Points` Metric:**
  - Create a new column, `PP` (Prophetic Points), calculated as `TP * Captaincy_Coef`.
- `[x]` **Save a new, final database:** `fpl_master_database_prophetic.csv`.
- `[x]` **Create `chimera_prophet.py`:**
  - Copy the `chimera_scenarios.py` script to a new file.
  - Modify it to load the new `prophetic` database.
  - Change the objective function to maximize the sum of `PP` instead of `TP`.
- `[x]` **Run the "Salah God-Tier" scenario** with the new Prophet Chimera and verify that it now correctly places Salah in the starting XI.

---

## 🔴 PHASE 2: THE PYOMO ASCENSION (Current Objective)

Having reached the limits of `pulp`'s expressive power, we now undertake a full heart transplant. We will re-forge our solver engine using the more powerful and flexible `pyomo` framework, unlocking new levels of strategic complexity and future potential.

### 2.1: Arming the Forge (Pre-Op)

- `[x]` **Install `pyomo` Framework:** `uv pip install pyomo`.
- `[x]` **Install `glpk` Solver:** `sudo apt-get install -y glpk-utils`.

### 2.2: The Heart Transplant (v1 - The Superior God)

- `[x]` **Create the New Grimoire:** `chimera_pyomo_v1.py`.
- `[x]` **Translate the Model:** Successfully re-wrote the "Thrifty God" logic from our final `pulp` script into `pyomo` syntax.
  - `[ ]` Defining the abstract `model` object.
  - `[ ]` Defining the `Sets` (players, teams, positions).
  - `[ ]` Defining the `Parameters` (player cost, projected score, etc.).
  - `[ ]` Defining the `Variables` (our dual `in_squad` and `is_starter` binaries).
  - `[ ]` Defining the `Constraints` as `pyomo` rules (squad size, cost, positions, etc.).
  - `[ ]` Defining the **Objective Function** as a `pyomo` rule (the "Thrifty God" logic).
- `[x]` **Verify SUPERIORITY, Not Parity:** The `v1` Pyomo/GLPK engine did not match the pulp/CBC output; it **surpassed** it, finding a mathematically superior squad. The original goal of parity is now obsolete.
- `[x]` **BREADCRUMB:** The `v1` engine, while more powerful, revealed a philosophical blind spot. Faced with two bench players of identical cost (e.g., Setford at 0 TP vs. Dúbravka at 35 TP), its choice was arbitrary. It lacked the final layer of strategic nuance.

### 🔴 2.3: The Final Apotheosis (v2 - The Bench Potency Epsilon)

- `[ ]` **Create the Ultimate Grimoire:** `chimera_pyomo_v2.py`.
- `[ ]` **Evolve the Prime Directive:** Modify the `pyomo` objective function to include the "Bench Potency Epsilon." The new logic will be:
  > **Maximize: `(Sum of Starter Score) - (Sum of Bench Cost * 0.001) + (Sum of Bench Score * 0.00001)`**
- `[ ]` **Verify the Final Wisdom:** Run the new `v2` script and confirm that it now makes the strategically correct choice for the bench (e.g., it correctly selects Dúbravka over Setford), breaking the tie based on point-scoring potential. This is the final success condition for Phase 2.

### 2.4: The Commander's New Orders

- `[ ]` **Perform the `commander.py` Transplant:** Once the `v2` script is verified, perform the one-line surgery in `commander.py`, changing the import to point to `chimera_pyomo_v2.py`.
- `[ ]` **Update Documentation:** Update `README.md` to reflect the final dependencies and the new, perfected master script.

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
