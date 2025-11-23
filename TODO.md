# PROJECT: BAMF DOMINATOR - STRATEGIC BLUEPRINT (v1.8)

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

- `[x]` **BREADCRUMB:** The simulations were a monumental success but revealed the Chimera's final, critical flaw: "Captaincy Blindness."

### 1.4: Granting Sight (The Captaincy Coefficient)

- `[x]` **Create `enrich_with_insight.py`** to inject our `(π)` strategic knowledge.
- `[x]` **Define the "Captaincy Coefficient"** and create the `Prophetic_Points` (`PP`) metric.
- `[x]` **Create `chimera_prophet.py`** to utilize the new metric.
- `[x]` **BREADCRUMB:** The Prophet Chimera correctly placed Salah in the starting XI, proving the value of `PP`.

---

## ✅ PHASE 1.5: REALITY RECONCILIATION (Completed)

- `[x]` **Acknowledge Personal History:** Create `squad.csv` to track our actual squad and purchase prices.
- `[x]` **Forge the Reality Bender:** Create `update_prices.py` script to inject our purchase prices into the market data, ensuring our budget is calculated against _our_ reality, not the market's.
- `[x]` **Update Workflow:** Integrate this as a new, mandatory pre-processing step before running the main gauntlet.

---

## ✅ PHASE 2: THE PYOMO ASCENSION (Completed)

Having reached the limits of `pulp`'s expressive power, we have completed a full heart transplant. We have re-forged our solver engine using the more powerful and flexible `pyomo` framework, unlocking new levels of strategic complexity and future potential.

### 2.1: Arming the Forge (Pre-Op)

- `[x]` **Install `pyomo` Framework:** `uv pip install pyomo`.
- `[x]` **Install `glpk` Solver:** `sudo apt-get install -y glpk-utils`.

### 2.2: The Heart Transplant (v1 - The Superior God)

- `[x]` **Create the New Grimoire:** `chimera_pyomo_v1.py`.
- `[x]` **Translate the Model:** Successfully re-wrote the "Thrifty God" logic from our final `pulp` script into `pyomo` syntax.
- `[x]` **Verify SUPERIORITY, Not Parity:** The `v1` Pyomo/GLPK engine surpassed the pulp/CBC output.
- `[x]` **BREADCRUMB:** The `v1` engine, while more powerful, revealed a philosophical blind spot in choosing between bench players of identical cost but different potential.

### 2.3: The Final Apotheosis (v2 - The Bench Potency Epsilon)

- `[x]` **Create the Ultimate Grimoire:** `chimera_pyomo_v2.py`.
- `[x]` **Evolve the Prime Directive:** Modified the `pyomo` objective function to include the "Bench Potency Epsilon."
- `[x]` **Verify the Final Wisdom:** Confirmed that the `v2` script now makes the strategically correct choice for the bench.

### 2.4: The Commander's New Orders

- `[x]` **Perform the `commander.py` Transplant:** Refactored `commander.py` to orchestrate the full pipeline, including the dual-solver reality.
- `[x]` **Update Documentation:** Updated `README.md` to reflect the final dependencies and the new, perfected master script.

---

## ✅ PHASE 3: THE COMMAND DECK (Completed)

The final phase: building the elegant, powerful, and interactive command center from which we will wield the Chimera's power.

### 3.1: Forge the Scepter (Master Orchestration Script)

- `[x]` **Create `commander.py`:** A single, top-level script that orchestrates the entire data pipeline.
- `[x]` **Refactor Core Scripts:** Ensure all pipeline scripts are importable and can be commanded.
- `[x]` **Add "Stage 0" Auto-Cleaning:** The Commander now purges old database files before each run.
- `[x]` **Add "Stage 6" Auto-Scribing:** The Commander now captures solver outputs and saves them to `squad_prophecy.md`.
- `[x]` **BREADCRUMB:** The Scepter is forged and powerful. We have a "one script to rule them all," but it is not yet a true, flexible Command Deck.

### 3.2: Build the Throne (Full CLI Implementation)

- `[x]` **Choose a Framework:** `click` has been chosen for its power and elegance.
- `[x]` **Create the `bamf` CLI:** The `bamf.py` script is our new entry point.
  - `[x]` `run-gauntlet`: The primary command is forged and functional.
  - `[x]` `init`: A helper command to create the new gameweek vault is complete.
  - `[x]` `run-scenario`: An interactive command to run "what-if" simulations with flags for including/excluding players.
  - `[x]` `audit`: Sub-commands for auditing team names (`teams`) and player names (`players`) are complete.

---

## ✅ PHASE 4: AUTOMATED DATA EXTRACTION (Completed)

The next frontier: automating the tedious manual data entry by leveraging Gemini Vision.

- `[x]` **Develop Gemini Vision Processor:** Create `process_screenshots.sh` to automate calls to the Gemini CLI for screenshot processing.
- `[x]` **Define Screenshot Naming Convention:** Established clear guidelines for screenshot filenames.
- `[x]` **Integrate into Weekly Ritual:** Updated `README.md` to include the new automated step.

---

## 🔴 PHASE 5: THE TRINITY OPTIMIZATION (FDR Refinement)

We have evolved our data intelligence. We no longer use a simple 1-5 Difficulty rating. We have secured **The Trinity**: `FDR` (Overall), `FDR_A` (Attack), and `FDR_D` (Defence), all calibrated on a high-precision **1000 (Easy) to 1400 (Hard)** scale. We must now upgrade the pipeline to utilize this granular tactical data.

- `[ ]` **Update the Cauldron (`forge_cauldron.py`):**
  - `[ ]` Update logic to ingest `fixtures.csv` with new headers: `Team,Gameweek,Opponent,Location,FDR,FDR_A,FDR_D`.
  - `[ ]` Implement the **Positional Bifurcation Logic**:
    - If Position is **GKP** or **DEF** -> Use `FDR_D`.
    - If Position is **MID** or **FWD** -> Use `FDR_A`.
    - Create a new unified column: `Effective_FDR_Raw`.
- `[ ]` **Normalize the Scale:**
  - `[ ]` Design a normalization function to translate the raw **1000-1400** scale into a format the solver can digest effectively (e.g., 0.0 to 1.0 or a normalized penalty score), replacing the old 1-5 integer scale.
  - `[ ]` _Goal:_ Ensure "Hard" fixtures still penalize selection probability or count towards difficulty limits, without breaking existing constraints.
- `[ ]` **Refactor the Solver (`chimera_pyomo_v2.py`):**
  - `[ ]` Update constraints that rely on FDR (e.g., "Don't pick more than X players with FDR > Y").
  - `[ ]` Determine the new threshold for a "Red Zone" fixture based on the 1000-1400 scale (likely > 1300).
- `[ ]` **Verify The Trinity:** Run the gauntlet and verify that Defenders are punished for playing Man City (High FDR_D), while Attackers are rewarded for playing Luton (Low FDR_A).

---

### NDH GLYPH KEY

- `⊕ (forge)`: The act of creation, building, synthesis.
- `⇌ (barb)`: Our shared forward voyage of discovery and collaboration.
- `⁂ (fungi)`: Mycelial, distributed, underlying network/intelligence.
- `π (pie)`: The Carbon Pirate (human) element; our strategic insight.
- `⌑ (mole)`: A strategic retreat or putting a task on the back-burner.
