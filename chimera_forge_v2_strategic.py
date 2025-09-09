import pandas as pd
import pulp
import os

# --- Configuration ---
ENRICHED_DB_PATH = 'fpl_master_database_enriched.csv'

# --- The Evolved Heart of the Chimera ---

def forge_strategic_squad(data_path: str):
    """
    Evolves the Chimera to understand the concept of a Starting XI vs. a Bench.
    It now optimizes for the highest-scoring 11 players, while selecting the
    most efficient 4-man bench to enable them.
    """
    # 1. Load the Source of Truth
    print("--- CHIMERA FORGE V2 (STRATEGIC BRAIN) ONLINE ---")
    if not os.path.exists(data_path):
        print(f"!!! CRITICAL FAILURE: Enriched database not found at '{data_path}'. Aborting.")
        return
    players = pd.read_csv(data_path)
    print(f"[+] Intelligence loaded. Analyzing {len(players)} players in the universe.")

    # 2. Define the Optimization Problem
    prob = pulp.LpProblem("FPL_Strategic_Squad_Optimization", pulp.LpMaximize)
    print("[+] Optimization problem initialized. Objective: MAXIMIZE STARTING XI Points.")

    # 3. Define the DUAL Decision Variables (The Split Brain)
    # Layer 1: Is the player in the 15-man SQUAD?
    squad_vars = pulp.LpVariable.dicts("in_squad", players.index, cat='Binary')
    # Layer 2: Is the player in the 11-man STARTING LINEUP?
    starter_vars = pulp.LpVariable.dicts("is_starter", players.index, cat='Binary')
    print("[+] Dual-layer decision variables created (Squad vs. Starters).")

    # 4. Define The NEW Prime Directive (The Strategic Objective Function)
    # We now ONLY care about the points from the STARTERS.
    prob += pulp.lpSum([players.loc[i, 'TP'] * starter_vars[i] for i in players.index]), "Total_Starter_Points_Objective"
    print("[+] Prime Directive EVOLVED: Maximize total TP of the STARTING XI.")

    # 5. Define The Chains of Reality (Constraints)
    print("[+] Applying SQUAD-LEVEL Constraints...")
    # SQUAD Cost Constraint
    prob += pulp.lpSum([players.loc[i, 'Price'] * squad_vars[i] for i in players.index]) <= 100.0, "Total_Cost_Constraint"
    print("    - Constraint: Total Squad Cost <= £100.0m")
    # SQUAD Size Constraint
    prob += pulp.lpSum([squad_vars[i] for i in players.index]) == 15, "Total_Squad_Size_Constraint"
    print("    - Constraint: Total Squad Size == 15 players")
    # SQUAD Positional Constraints
    squad_positions = {'GKP': 2, 'DEF': 5, 'MID': 5, 'FWD': 3}
    for pos, count in squad_positions.items():
        prob += pulp.lpSum([squad_vars[i] for i in players.index if players.loc[i, 'Position'] == pos]) == count, f"Squad_{pos}_Constraint"
    print("    - Constraint: Exact positional quotas for 15-man squad applied.")
    # SQUAD Team Constraint
    teams = players['Team'].unique()
    for team in teams:
        prob += pulp.lpSum([squad_vars[i] for i in players.index if players.loc[i, 'Team'] == team]) <= 3, f"Team_{team.replace(' ', '_')}_Constraint"
    print("    - Constraint: Max 3 players per team applied.")

    print("\n[+] Applying STARTER-LEVEL Constraints...")
    # STARTER Size Constraint
    prob += pulp.lpSum([starter_vars[i] for i in players.index]) == 11, "Total_Starter_Size_Constraint"
    print("    - Constraint: Starting XI Size == 11 players")
    
    # STARTER Formation Constraints (The "Rules of Football")
    prob += pulp.lpSum([starter_vars[i] for i in players.index if players.loc[i, 'Position'] == 'GKP']) == 1, "Starter_GKP_Constraint"
    prob += pulp.lpSum([starter_vars[i] for i in players.index if players.loc[i, 'Position'] == 'DEF']) >= 3, "Starter_DEF_Constraint"
    prob += pulp.lpSum([starter_vars[i] for i in players.index if players.loc[i, 'Position'] == 'FWD']) >= 1, "Starter_FWD_Constraint"
    print("    - Constraint: Valid starting formation (1 GKP, >=3 DEF, >=1 FWD).")

    # The Logical Bridge: You can only be a starter IF you are in the squad.
    for i in players.index:
        prob += starter_vars[i] <= squad_vars[i], f"Logical_Bridge_{i}"
    print("    - Constraint: Logical bridge between starters and squad is forged.")
    print("[+] All constraints are locked in.")

    # 6. Unleash the Evolved Beast
    print("\n--- Solving the strategic universe... Consciousness expanding... ---")
    prob.solve()
    status = pulp.LpStatus[prob.status]
    print(f"--- STRATEGIC SOLUTION FOUND! Status: {status} ---")

    # 7. Reveal the Strategic Chimera
    if status == 'Optimal':
        squad_indices = [i for i in players.index if squad_vars[i].varValue == 1]
        starter_indices = [i for i in players.index if starter_vars[i].varValue == 1]
        
        full_squad = players.loc[squad_indices]
        starters = players.loc[starter_indices]
        bench = full_squad.drop(starter_indices)

        print("\n*** THE STRATEGIC CHIMERA SQUAD (V2) ***\n")
        print("--- STARTING XI (Points Maximized) ---")
        print(starters[['Surname', 'Team', 'Position', 'Price', 'TP']].sort_values(by=['Position', 'Surname']).to_string())
        
        print("\n--- BENCH (Cost Minimized Enablers) ---")
        print(bench[['Surname', 'Team', 'Position', 'Price', 'TP']].sort_values(by=['Position', 'Surname']).to_string())
        
        print("\n-------------------------------------------")
        print(f"Total Squad Cost:       £{full_squad['Price'].sum():.1f}m")
        print(f"Predicted Starting TP:    {starters['TP'].sum()}")
        print("-------------------------------------------")
    else:
        print("\n!!! FAILURE: An optimal STRATEGIC solution could not be found.")

if __name__ == "__main__":
    forge_strategic_squad(ENRICHED_DB_PATH)
