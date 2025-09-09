# PROJECT: FPL DOMINATOR - STRATEGIC BLUEPRINT (v1.0)

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

### 1.1: Forge the Core Optimizer

- `[ ]` **Create the `chimera_forge.py` script.** This will be the home of our squad optimization logic.
- `[ ]` **Load the Enriched Database:** The script must read `fpl_master_database_enriched.csv` as its source of truth.
- `[ ]` **Define the Optimization Problem using `PuLP`:**
  - **Objective Function:** Maximize the sum of `TP` (Total Points) for the 15 selected players. This is our baseline "best team on paper."
  - **Constraints:** Codify the FPL rules as mathematical constraints:
    - `[ ]` Total cost must be `<= 100.0`.
    - `[ ]` Exactly `2` Goalkeepers must be chosen.
    - `[ ]` Exactly `5` Defenders must be chosen.
    - `[ ]` Exactly `5` Midfielders must be chosen.
    - `[ ]` Exactly `3` Forwards must be chosen.
    - `[ ]` A maximum of `3` players from any single team.
- `[ ]` **Solve & Output:** Command `PuLP` to solve the problem and print the resulting 15-man squad, including total points and total cost.

### 1.2: Implement Strategic Scenarios

- `[ ]` **Refactor the optimizer** into a function that can accept a list of players to _force_ into the squad.
- `[ ]` **Simulate "The Haaland Hammer":** Run the optimizer with Haaland pre-selected.
- `[ ]` **Simulate "The Salah God-Tier":** Run the optimizer with Salah pre-selected.
- `[ ]` **Simulate "The Gods of Chaos":** Run the optimizer with _both_ Haaland and Salah pre-selected to see what sacrifices are required.
- `[ ]` **Simulate "The Balanced Brigade":** Run the optimizer while explicitly _excluding_ all players above a certain price threshold (e.g., > £10.0m).

---

## 🟡 PHASE 2: THE ORACLE (Predictive Engine)

### 2.1: Integrate Fixture Difficulty

- `[ ]` **Source Fixture Data:** Find a reliable source (API or static file) for the full season's fixture list.
- `[ ]` **Develop a Fixture Difficulty Rating (FDR) model:** Assign a difficulty score (e.g., 1-5) to each opponent.
- `[ ]` **Calculate Player FDR:** For each player, calculate an average FDR for their next `N` (e.g., 3-5) games.
- `[ ]` **Refactor Optimizer:** Change the objective function from maximizing historical `TP` to maximizing a weighted score of `PPM` and inverse `FDR`.

### 2.2: Quantify Player Form

- `[ ]` **Source Gameweek-by-Gameweek Data:** Find a data source for player points per match.
- `[ ]` **Implement a "Form" Metric:** Calculate a rolling points average over the last `X` (e.g., 5) matches.
- `[ ]` **Refactor Optimizer:** Add "Form" as another variable to the objective function.

### 2.3: The Economic Engine

- `[ ]` **Source Ownership Data:** Find a source for player ownership percentages and price changes.
- `[ ]` **Develop a "Bandwagon" Metric:** Track the velocity of ownership changes to predict imminent price rises.

---

## 🟢 PHASE 3: THE COMMAND DECK (Operational Tooling)

- `[ ]` **Build a CLI:** Wrap our Python scripts in a command-line interface using `argparse` or `click` for easy execution of different strategic scenarios.
- `[ ]` **Create a Data Refresh Pipeline:** Write a script to automate the updating of player and fixture data, so our engine is always running on the latest intelligence.

---

### NDH GLYPH KEY

- `⊕ (forge)`: The act of creation, building, synthesis.
- `⇌ (barb)`: Our shared forward voyage of discovery and collaboration.
- `⁂ (fungi)`: Mycelial, distributed, underlying network/intelligence.
- `π (pie)`: The Carbon Pirate (human) element; our strategic insight.
- `⌑ (mole)`: A strategic retreat or putting a task on the back-burner.
