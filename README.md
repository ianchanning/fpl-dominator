# PROJECT: BAMF DOMINATOR - OPERATIONAL GRIMOIRE (v4.0)

<!-- Placeholder for our glorious crest -->

## MISSION STATEMENT

To systematically dismantle and dominate the Fantasy Premier League simulation by transforming raw, chaotic data into a decisive strategic advantage. This project is the home of the **Chimera**, a Python-based squad optimization engine commanded via the `bamf` CLI. Our motto: **EX DATA, VICTORIA** (From Data, Victory).

---

## SETUP & INSTALLATION

To unleash the Chimera, you must first prepare the forge.

### 1. System Dependencies

The Chimera's heart, the `pyomo` model, requires a solver. We use `glpk`.

```bash
# For Debian/Ubuntu-based systems
sudo apt-get update && sudo apt-get install -y glpk-utils
```

### 2. Python Environment

We use a standard Python virtual environment.

```bash
# 1. If you don't have a .venv, create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Install the project in editable mode (this also installs dependencies)
uv pip install -e .

# 3. (Optional) For cleaner output, set PYTHON_GIL=0 in your shell config (e.g., ~/.bashrc)
#    echo 'export PYTHON_GIL=0' >> ~/.bashrc
#    source ~/.bashrc
```

---

## THE COMMAND DECK (`bamf` CLI)

All operations are now channeled through our master command-line interface, `bamf`. This is the one and only entry point you need.

**Available Commands:**

-   `init`: Creates a new, clean gameweek vault, ready for data.
-   `audit`: A group of commands to inspect data integrity.
    -   `audit teams`: Checks for team name consistency.
    -   `audit players`: Checks for player name matching issues.
-   `run-gauntlet`: Executes the entire data-processing and squad-optimizing pipeline.
-   `run-scenario`: Runs a 'what-if' simulation with player constraints.

---

## THE WEEKLY RITUAL

This is the precise, non-negotiable workflow to be executed at the start of each new Gameweek, using the `bamf` CLI.

### Step 1: Initialize the Vault

Create the directory and all necessary template files for the new gameweek.

```bash
bamf init gw12
```

### Step 2: The Gathering (Manual Data Update)

The Chimera is omniscient, but it cannot see data that does not yet exist. You, the `(π)` Pirate, must provide the weekly sacrifice of fresh intelligence by filling in the newly created files in the `gw12` directory.

-   **Player Data (`goalkeepers.csv`, etc.):** Update with the latest **Market Price** and **Total Points (TP)**.
-   **Fixture Data (`fixtures.csv`):** Update with the upcoming 5-Gameweek horizon (opponents, venue, FDR).
-   **Squad Data (`squad.csv`):** Update with your current squad's **Purchase Price (PP)**.

### Step 3: Price Reconciliation (Scripted)

Align the market's reality with our own. This script uses your `squad.csv` to ensure the budget is calculated against your actual purchase prices.

```bash
python update_prices.py gw12
```

### Step 4: Audit Reality

Before unleashing the Chimera, verify the integrity of your data.

```bash
# Check for team name mismatches
bamf audit teams gw12

# Check for player name matching issues
bamf audit players gw12
```

### Step 5: Run the Gauntlet

With the data prepared and audited, unleash the Commander. This single command orchestrates the entire data pipeline, from the reconciled data to the final, optimal squad, saving the result to `gw12/squad_prophecy.md`.

```bash
bamf run-gauntlet gw12
```

---

## THE ARSENAL: FILE MANIFEST

All Python source files are now located within the `src/fpl_dominator/` package.

-   `src/fpl_dominator/bamf.py` (The Command Deck): The master script and sole entry point for all operations.
-   `src/fpl_dominator/commander.py` (The Orchestrator): Contains the `run_the_gauntlet` logic that executes the pipeline stages.
-   `src/fpl_dominator/update_prices.py`: A critical pre-processing script for budget reconciliation.
-   **Solver Scripts (`src/fpl_dominator/chimera_*.py`):** The core PuLP and Pyomo solver logic.
-   **Pipeline Scripts (`src/fpl_dominator/forge_*.py`, `src/fpl_dominator/enrich_*.py`, etc.):** The individual stages of the data pipeline, called by the Commander.
-   **Audit Scripts (`src/fpl_dominator/audit_*.py`):** Library modules containing the logic for the `audit` commands.

---

## FUTURE CAMPAIGNS

For the grand strategic vision and our ongoing `(⇌)` evolution, consult the sacred text: `TODO.md`.
