import pandas as pd
import pulp
import os
import sys

if len(sys.argv) != 2:
    print(">>> ERROR: A gameweek directory must be provided.")
    print(">>> USAGE: python chimera_final_form_v5_rosetta.py gw4")
    sys.exit(1)

# --- Configuration ---
GAMEWEEK_DIR = sys.argv[1]
OMNISCIENT_DB_PATH = f'{GAMEWEEK_DIR}/fpl_master_database_OMNISCIENT.csv' # <-- The ULTIMATE source of truth
THRIFT_FACTOR = 0.001

# --- CORE FUNCTIONS (Unchanged, but now wielding ultimate power) ---

def print_squad_details(squad, starters, bench, status, scenario_name):
    print(f"\n{'='*20} {scenario_name.upper()} {'='*20}")
    if status == 'Optimal':
        print("\n*** ORACLE SQUAD FORGED (OPTIMIZED FOR GW4-GW8) ***\n")
        print("--- STARTING XI (Projected Score Maximized) ---")
        print(starters[['Surname', 'Team', 'Position', 'Price', 'PP', 'Projected_Score']].sort_values(by=['Position', 'Projected_Score'], ascending=[True, False]).to_string(index=False))
        print("\n--- BENCH (RUTHLESSLY Cost-Optimized) ---")
        print(bench[['Surname', 'Team', 'Position', 'Price', 'PP', 'Projected_Score']].sort_values(by=['Position', 'Price']).to_string(index=False))
        print("\n-------------------------------------------")
        print(f"Total Squad Cost:          £{squad['Price'].sum():.1f}m")
        print(f"Projected Starting Score:    {starters['Projected_Score'].sum():.2f}")
        print(f"Money in the Bank:         £{100.0 - squad['Price'].sum():.1f}m")
        print("-------------------------------------------")
    else:
        print(f"\n!!! FAILURE: An optimal ORACLE solution could not be found. Status: {status}")
    print(f"{'='* (42 + len(scenario_name))}")

def forge_oracle_squad(players_df, scenario_name):
    """
    The Oracle Chimera. Forges an optimal squad based on Projected Score over the horizon.
    """
    print(f"\n>>> LAUNCHING ORACLE SIMULATION: {scenario_name}...")
    prob = pulp.LpProblem(f"FPL_Oracle_{scenario_name.replace(' ', '_')}", pulp.LpMaximize)
    
    squad_vars = pulp.LpVariable.dicts("in_squad", players_df.index, cat='Binary')
    starter_vars = pulp.LpVariable.dicts("is_starter", players_df.index, cat='Binary')

    # --- THE FINAL, OMNISCIENT OBJECTIVE FUNCTION ---
    # We now maximize 'Projected_Score' instead of 'PP' or 'TP'.
    starter_projected_score = pulp.lpSum([players_df.loc[i, 'Projected_Score'] * starter_vars[i] for i in players_df.index])
    bench_cost_penalty = pulp.lpSum([(squad_vars[i] - starter_vars[i]) * players_df.loc[i, 'Price'] * THRIFT_FACTOR for i in players_df.index])
    prob += starter_projected_score - bench_cost_penalty, "Oracle_God_Objective"

    # --- Constraints are identical to the Thrifty God ---
    # (The logic of squad building is eternal, only the objective changes)
    prob += pulp.lpSum([players_df.loc[i, 'Price'] * squad_vars[i] for i in players_df.index]) <= 100.0, "Cost"
    prob += pulp.lpSum([squad_vars[i] for i in players_df.index]) == 15, "SquadSize"
    for pos, count in {'GKP': 2, 'DEF': 5, 'MID': 5, 'FWD': 3}.items():
        prob += pulp.lpSum([squad_vars[i] for i in players_df.index if players_df.loc[i, 'Position'] == pos]) == count, f"Squad_{pos}"
    for team in players_df['Team_TLA'].unique():
        prob += pulp.lpSum([squad_vars[i] for i in players_df.index if players_df.loc[i, 'Team_TLA'] == team]) <= 3, f"Team_{team.replace(' ', '_')}"
    prob += pulp.lpSum([starter_vars[i] for i in players_df.index]) == 11, "StarterSize"
    prob += pulp.lpSum([starter_vars[i] for i in players_df.index if players_df.loc[i, 'Position'] == 'GKP']) == 1, "Starter_GKP"
    prob += pulp.lpSum([starter_vars[i] for i in players_df.index if players_df.loc[i, 'Position'] == 'DEF']) >= 3, "Starter_DEF"
    prob += pulp.lpSum([starter_vars[i] for i in players_df.index if players_df.loc[i, 'Position'] == 'FWD']) >= 1, "Starter_FWD"
    for i in players_df.index: prob += starter_vars[i] <= squad_vars[i], f"Bridge_{i}"

    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    status = pulp.LpStatus[prob.status]

    squad_indices = [i for i in players_df.index if squad_vars[i].varValue == 1]
    starter_indices = [i for i in players_df.index if starter_vars[i].varValue == 1]
    squad = players_df.loc[squad_indices]
    starters = players_df.loc[starter_indices]
    bench = squad.drop(starter_indices)
    
    print_squad_details(squad, starters, bench, status, scenario_name)

# --- Main Execution Block: The Final Prophecy ---
if __name__ == "__main__":
    print("--- CHIMERA ORACLE ENGINE ONLINE ---")
    if not os.path.exists(OMNISCIENT_DB_PATH):
        print(f"!!! CRITICAL FAILURE: Omniscient Database not found at '{OMNISCIENT_DB_PATH}'. Aborting.")
    else:
        players = pd.read_csv(OMNISCIENT_DB_PATH)
        forge_oracle_squad(players, "Optimal Squad for GW4-GW8")
