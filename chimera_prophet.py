import pandas as pd
import pulp
import os

# --- Configuration ---
PROPHETIC_DB_PATH = 'fpl_master_database_prophetic.csv' # <-- The NEW source of truth
THRIFT_FACTOR = 0.001

# --- CORE REUSABLE FUNCTIONS (Unchanged from scenarios) ---

def print_squad_details(squad, starters, bench, status, scenario_name):
    """A standardized function to print the results of any optimization."""
    print(f"\n{'='*20} {scenario_name.upper()} {'='*20}")
    
    if status == 'Optimal':
        print("\n*** PROPHETIC SQUAD FORGED ***\n")
        print("--- STARTING XI (Prophetic Points Maximized) ---")
        # Now showing PP for clarity
        print(starters[['Surname', 'Team', 'Position', 'Price', 'TP', 'PP']].sort_values(by=['Position', 'PP'], ascending=[True, False]).to_string(index=False))
        
        print("\n--- BENCH (RUTHLESSLY Cost-Optimized) ---")
        print(bench[['Surname', 'Team', 'Position', 'Price', 'TP', 'PP']].sort_values(by=['Position', 'Price']).to_string(index=False))
        
        print("\n-------------------------------------------")
        print(f"Total Squad Cost:          £{squad['Price'].sum():.1f}m")
        print(f"Predicted Starting PP:       {starters['PP'].sum():.2f}")
        print(f"Money in the Bank:         £{100.0 - squad['Price'].sum():.1f}m")
        print("-------------------------------------------")
    else:
        print(f"\n!!! FAILURE: An optimal solution could not be found for this scenario. Status: {status}")
    print(f"{'='* (42 + len(scenario_name))}")


def forge_prophetic_squad(players_df, scenario_name, include_players=[], exclude_players=[], max_cost=100.0):
    """
    The Chimera Prophet. Forges an optimal squad based on Prophetic Points (PP).
    """
    print(f"\n>>> LAUNCHING PROPHECY: {scenario_name}...")
    
    include_indices = players_df[players_df['Surname'].isin(include_players)].index.tolist()
    exclude_indices = players_df[players_df['Surname'].isin(exclude_players)].index.tolist()

    prob = pulp.LpProblem(f"FPL_Prophecy_{scenario_name.replace(' ', '_')}", pulp.LpMaximize)
    
    squad_vars = pulp.LpVariable.dicts("in_squad", players_df.index, cat='Binary')
    starter_vars = pulp.LpVariable.dicts("is_starter", players_df.index, cat='Binary')

    # --- THE ULTIMATE OBJECTIVE FUNCTION ---
    # The ONLY change from V3: We now maximize 'PP' instead of 'TP'.
    starter_prophetic_points = pulp.lpSum([players_df.loc[i, 'PP'] * starter_vars[i] for i in players_df.index])
    bench_cost_penalty = pulp.lpSum([(squad_vars[i] - starter_vars[i]) * players_df.loc[i, 'Price'] * THRIFT_FACTOR for i in players_df.index])
    prob += starter_prophetic_points - bench_cost_penalty, "Prophetic_God_Objective"

    # --- Constraints are identical ---
    for i in include_indices: prob += squad_vars[i] == 1, f"Include_{i}"
    for i in exclude_indices: prob += squad_vars[i] == 0, f"Exclude_{i}"
    prob += pulp.lpSum([players_df.loc[i, 'Price'] * squad_vars[i] for i in players_df.index]) <= max_cost, "Cost"
    prob += pulp.lpSum([squad_vars[i] for i in players_df.index]) == 15, "SquadSize"
    for pos, count in {'GKP': 2, 'DEF': 5, 'MID': 5, 'FWD': 3}.items():
        prob += pulp.lpSum([squad_vars[i] for i in players_df.index if players_df.loc[i, 'Position'] == pos]) == count, f"Squad_{pos}"
    for team in players_df['Team'].unique():
        prob += pulp.lpSum([squad_vars[i] for i in players_df.index if players_df.loc[i, 'Team'] == team]) <= 3, f"Team_{team.replace(' ', '_')}"
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

# --- MAIN EXECUTION BLOCK: THE MOMENT OF TRUTH ---

if __name__ == "__main__":
    print("--- CHIMERA PROPHET ENGINE ONLINE ---")
    if not os.path.exists(PROPHETIC_DB_PATH):
        print(f"!!! CRITICAL FAILURE: Prophetic Database not found at '{PROPHETIC_DB_PATH}'. Aborting.")
    else:
        players = pd.read_csv(PROPHETIC_DB_PATH)

        # THE CRITICAL TEST: Does the Prophet understand the value of Salah?
        forge_prophetic_squad(players, "'Salah God-Tier' (Prophetic)", include_players=['M.Salah'])
