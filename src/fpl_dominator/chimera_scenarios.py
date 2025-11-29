import os
import sys

import pandas as pd
import pulp

if len(sys.argv) != 2:
    print(">>> ERROR: A gameweek directory must be provided.")
    print(">>> USAGE: python chimera_final_form_v5_rosetta.py gw4")
    sys.exit(1)

# --- Configuration ---
GAMEWEEK_DIR = sys.argv[1]
ENRICHED_DB_PATH = f"{GAMEWEEK_DIR}/fpl_master_database_enriched.csv"
THRIFT_FACTOR = 0.001

# --- CORE REUSABLE FUNCTIONS ---


def print_squad_details(squad, starters, bench, status, scenario_name):
    """A standardized function to print the results of any optimization."""
    print(f"\n{'='*20} {scenario_name.upper()} {'='*20}")

    if status == "Optimal":
        print("\n*** OPTIMAL SQUAD FORGED ***\n")
        print("--- STARTING XI (Points Maximized) ---")
        print(
            starters[["Surname", "Team", "Position", "Price", "TP"]]
            .sort_values(by=["Position", "TP"], ascending=[True, False])
            .to_string(index=False)
        )

        print("\n--- BENCH (RUTHLESSLY Cost-Optimized) ---")
        print(
            bench[["Surname", "Team", "Position", "Price", "TP"]]
            .sort_values(by=["Position", "Price"])
            .to_string(index=False)
        )

        print("\n-------------------------------------------")
        print(f"Total Squad Cost:       £{squad['Price'].sum():.1f}m")
        print(f"Predicted Starting TP:    {starters['TP'].sum()}")
        print(f"Bench Cost:             £{bench['Price'].sum():.1f}m")
        print(f"Money in the Bank:      £{100.0 - squad['Price'].sum():.1f}m")
        print("-------------------------------------------")
    else:
        print(
            f"\n!!! FAILURE: An optimal solution could not be found for this scenario. Status: {status}"
        )
    print(f"{'='* (42 + len(scenario_name))}")


def forge_squad(
    players_df, scenario_name, include_players=[], exclude_players=[], max_cost=100.0
):
    """
    The heart of the Scenario Engine. Forges an optimal squad based on a given set of
    tactical constraints (inclusions, exclusions, budget).
    """
    print(f"\n>>> LAUNCHING SIMULATION: {scenario_name}...")

    # --- Filter players based on exclusions ---
    # Convert names to indices for PuLP
    exclude_indices = players_df[
        players_df["Surname"].isin(exclude_players)
    ].index.tolist()
    if exclude_indices:
        print(f"    - EXCLUDING {len(exclude_indices)} players from consideration.")

    include_indices = players_df[
        players_df["Surname"].isin(include_players)
    ].index.tolist()
    if include_indices:
        print(f"    - FORCING inclusion of {len(include_players)} players.")

    # --- Initialize the problem ---
    prob = pulp.LpProblem(
        f"FPL_Scenario_{scenario_name.replace(' ', '_')}", pulp.LpMaximize
    )

    squad_vars = pulp.LpVariable.dicts("in_squad", players_df.index, cat="Binary")
    starter_vars = pulp.LpVariable.dicts("is_starter", players_df.index, cat="Binary")

    # --- The "Thrifty God" Objective Function ---
    starter_points = pulp.lpSum(
        [players_df.loc[i, "TP"] * starter_vars[i] for i in players_df.index]
    )
    bench_cost_penalty = pulp.lpSum(
        [
            (squad_vars[i] - starter_vars[i])
            * players_df.loc[i, "Price"]
            * THRIFT_FACTOR
            for i in players_df.index
        ]
    )
    prob += starter_points - bench_cost_penalty, "Thrifty_God_Objective"

    # --- Apply Constraints ---
    # Tactical Constraints (Inclusions/Exclusions)
    for i in include_indices:
        prob += squad_vars[i] == 1, f"Force_Include_{i}"
    for i in exclude_indices:
        prob += squad_vars[i] == 0, f"Force_Exclude_{i}"

    # Standard Game Rule Constraints
    prob += (
        pulp.lpSum(
            [players_df.loc[i, "Price"] * squad_vars[i] for i in players_df.index]
        )
        <= max_cost,
        "Cost",
    )
    prob += pulp.lpSum([squad_vars[i] for i in players_df.index]) == 15, "SquadSize"
    for pos, count in {"GKP": 2, "DEF": 5, "MID": 5, "FWD": 3}.items():
        prob += (
            pulp.lpSum(
                [
                    squad_vars[i]
                    for i in players_df.index
                    if players_df.loc[i, "Position"] == pos
                ]
            )
            == count,
            f"Squad_{pos}",
        )
    for team in players_df["Team"].unique():
        prob += (
            pulp.lpSum(
                [
                    squad_vars[i]
                    for i in players_df.index
                    if players_df.loc[i, "Team"] == team
                ]
            )
            <= 3,
            f"Team_{team.replace(' ', '_')}",
        )
    prob += pulp.lpSum([starter_vars[i] for i in players_df.index]) == 11, "StarterSize"
    prob += (
        pulp.lpSum(
            [
                starter_vars[i]
                for i in players_df.index
                if players_df.loc[i, "Position"] == "GKP"
            ]
        )
        == 1,
        "Starter_GKP",
    )
    prob += (
        pulp.lpSum(
            [
                starter_vars[i]
                for i in players_df.index
                if players_df.loc[i, "Position"] == "DEF"
            ]
        )
        >= 3,
        "Starter_DEF",
    )
    prob += (
        pulp.lpSum(
            [
                starter_vars[i]
                for i in players_df.index
                if players_df.loc[i, "Position"] == "FWD"
            ]
        )
        >= 1,
        "Starter_FWD",
    )
    for i in players_df.index:
        prob += starter_vars[i] <= squad_vars[i], f"Bridge_{i}"

    # --- Solve and Print ---
    prob.solve(pulp.PULP_CBC_CMD(msg=0))  # msg=0 silences the verbose solver output
    status = pulp.LpStatus[prob.status]

    squad_indices = [i for i in players_df.index if squad_vars[i].varValue == 1]
    starter_indices = [i for i in players_df.index if starter_vars[i].varValue == 1]
    squad = players_df.loc[squad_indices]
    starters = players_df.loc[starter_indices]
    bench = squad.drop(starter_indices)

    print_squad_details(squad, starters, bench, status, scenario_name)


# --- MAIN EXECUTION BLOCK: THE TACTICAL WORKBENCH ---

if __name__ == "__main__":
    print("--- CHIMERA SCENARIO ENGINE ONLINE ---")
    if not os.path.exists(ENRICHED_DB_PATH):
        print(
            f"!!! CRITICAL FAILURE: Database not found at '{ENRICHED_DB_PATH}'. Aborting."
        )
    else:
        players = pd.read_csv(ENRICHED_DB_PATH)

        # SCENARIO 1: The Baseline "Thrifty God" (our perfected V3)
        forge_squad(players, "Baseline 'Thrifty God'")

        # SCENARIO 2: The "Haaland Hammer"
        forge_squad(players, "'Haaland Hammer'", include_players=["Haaland"])

        # SCENARIO 3: The "Salah God-Tier"
        # Handling the possibility Salah isn't in our limited dataset
        if "M.Salah" in players["Surname"].values:
            forge_squad(players, "'Salah God-Tier'", include_players=["M.Salah"])
        else:
            print(
                "\n>>> SKIPPING SCENARIO: 'Salah God-Tier' (M.Salah not in provided dataset)"
            )

        # SCENARIO 4: The "Gods of Chaos"
        if "M.Salah" in players["Surname"].values:
            forge_squad(
                players, "'Gods of Chaos'", include_players=["Haaland", "M.Salah"]
            )
        else:
            print(
                "\n>>> SKIPPING SCENARIO: 'Gods of Chaos' (M.Salah not in provided dataset)"
            )

        # SCENARIO 5: The "Balanced Brigade"
        high_priced_players = players[players["Price"] > 10.0]["Surname"].tolist()
        forge_squad(players, "'Balanced Brigade'", exclude_players=high_priced_players)
