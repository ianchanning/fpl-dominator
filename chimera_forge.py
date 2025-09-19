import pandas as pd
import pulp
import os

# --- Configuration ---
DIR = 'gw4'
ENRICHED_DB_PATH = f'{DIR}/fpl_master_database_enriched.csv'

# --- The Heart of the Chimera ---

def forge_optimal_squad(data_path: str):
    """
    Loads the enriched FPL database and uses PuLP to solve for the optimal
    15-man squad based on maximizing Total Points (TP) under all game constraints.
    """
    # 1. Load the Source of Truth
    print("--- CHIMERA FORGE ONLINE ---")
    if not os.path.exists(data_path):
        print(f"!!! CRITICAL FAILURE: Enriched database not found at '{data_path}'. Aborting.")
        return

    try:
        players = pd.read_csv(data_path)
        print(f"[+] Intelligence loaded. Analyzing {len(players)} players in the universe.")
    except Exception as e:
        print(f"!!! CRITICAL FAILURE: Could not read the database. Error: {e}")
        return

    # 2. Define the Optimization Problem
    # We are MAXIMIZING a value (Total Points).
    prob = pulp.LpProblem("FPL_Squad_Optimization", pulp.LpMaximize)
    print("[+] Optimization problem initialized. Objective: MAXIMIZE Total Points.")

    # 3. Define the Decision Variables
    # For each player, we must decide: are they in the squad (1) or not (0)?
    # This is a classic binary variable problem.
    decision_vars = pulp.LpVariable.dicts("player", players.index, cat='Binary')
    print("[+] Decision variables created for each player.")

    # 4. Define The Prime Directive (The Objective Function)
    # The goal is to maximize the sum of (TP of a player * their decision variable).
    prob += pulp.lpSum([players.loc[i, 'TP'] * decision_vars[i] for i in players.index]), "Total_Points_Objective"
    print("[+] Prime Directive set: Maximize total TP of the 15-man squad.")

    # 5. Define The Chains of Reality (The Constraints)
    print("[+] Applying the Chains of Reality (Game Constraints)...")
    
    # Cost Constraint
    prob += pulp.lpSum([players.loc[i, 'Price'] * decision_vars[i] for i in players.index]) <= 100.0, "Total_Cost_Constraint"
    print("    - Constraint Applied: Total Cost <= £100.0m")

    # Squad Size Constraint
    prob += pulp.lpSum([decision_vars[i] for i in players.index]) == 15, "Total_Players_Constraint"
    print("    - Constraint Applied: Total Squad Size == 15 players")

    # Positional Constraints
    positions = {'GKP': 2, 'DEF': 5, 'MID': 5, 'FWD': 3}
    for pos, count in positions.items():
        prob += pulp.lpSum([decision_vars[i] for i in players.index if players.loc[i, 'Position'] == pos]) == count, f"{pos}_Constraint"
        print(f"    - Constraint Applied: Exactly {count} players in position {pos}")

    # Team Constraint
    teams = players['Team'].unique()
    for team in teams:
        prob += pulp.lpSum([decision_vars[i] for i in players.index if players.loc[i, 'Team'] == team]) <= 3, f"Team_{team.replace(' ', '_')}_Constraint"
    print("    - Constraint Applied: Max 3 players per team for all teams.")
    print("[+] All constraints are locked in.")

    # 6. Unleash the Beast (Solve the Problem)
    print("\n--- Solving the universe... This may take a moment. ---")
    prob.solve()
    status = pulp.LpStatus[prob.status]
    print(f"--- SOLUTION FOUND! Status: {status} ---")

    # 7. Reveal the Chimera (Output the Results)
    if status == 'Optimal':
        selected_indices = [i for i in players.index if decision_vars[i].varValue == 1]
        squad = players.loc[selected_indices]

        total_cost = squad['Price'].sum()
        total_points = squad['TP'].sum()

        print("\n*** THE OPTIMAL CHIMERA SQUAD HAS BEEN FORGED ***\n")
        print(squad[['Surname', 'Team', 'Position', 'Price', 'TP']].to_string())
        print("\n-------------------------------------------------")
        print(f"Total Squad Cost: £{total_cost:.1f}m")
        print(f"Total Squad Points: {total_points}")
        print("-------------------------------------------------")
    else:
        print("\n!!! FAILURE: An optimal solution could not be found. The constraints may be impossible to satisfy.")

# --- Main Execution Block ---

if __name__ == "__main__":
    forge_optimal_squad(ENRICHED_DB_PATH)
