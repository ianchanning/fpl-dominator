import pandas as pd
import pulp
import os

# --- Configuration ---
DIR = 'gw3'
ENRICHED_DB_PATH = f'{DIR}/fpl_master_database_enriched.csv'
# The Cost Epsilon: A tiny penalty to encourage the cheapest bench as a tie-breaker.
THRIFT_FACTOR = 0.001

# --- The Final Form of the Chimera ---

def forge_thrifty_squad(data_path: str):
    """
    Evolves the Chimera into the "Thrifty God." It maximizes starter points while
    being mathematically compelled to select the cheapest possible bench.
    """
    # 1. Load the Source of Truth
    print("--- CHIMERA FORGE V3 (THRIFTY GOD) ONLINE ---")
    if not os.path.exists(data_path):
        print(f"!!! CRITICAL FAILURE: Enriched database not found at '{data_path}'. Aborting.")
        return
    players = pd.read_csv(data_path)
    print(f"[+] Intelligence loaded. Analyzing {len(players)} players in the universe.")

    # 2. Define the Optimization Problem
    prob = pulp.LpProblem("FPL_Thrifty_God_Optimization", pulp.LpMaximize)
    print("[+] Optimization problem initialized. Objective: MAXIMIZE Starter Points, MINIMIZE Bench Cost.")

    # 3. Define Dual Decision Variables
    squad_vars = pulp.LpVariable.dicts("in_squad", players.index, cat='Binary')
    starter_vars = pulp.LpVariable.dicts("is_starter", players.index, cat='Binary')
    print("[+] Dual-layer decision variables created (Squad vs. Starters).")

    # 4. Define The ULTIMATE Prime Directive (The Thrifty Objective Function)
    # This is the core evolution. We sum starter points and subtract a tiny fraction of the bench cost.
    # A player is on the bench if (in_squad - is_starter) == 1.
    starter_points = pulp.lpSum([players.loc[i, 'TP'] * starter_vars[i] for i in players.index])
    bench_cost_penalty = pulp.lpSum([(squad_vars[i] - starter_vars[i]) * players.loc[i, 'Price'] * THRIFT_FACTOR for i in players.index])
    
    prob += starter_points - bench_cost_penalty, "Thrifty_God_Objective"
    print("[+] Prime Directive EVOLVED: The Thrifty God objective is set.")

    # 5. Define The Chains of Reality (Constraints remain the same as V2)
    print("[+] Applying all SQUAD-LEVEL and STARTER-LEVEL constraints...")
    # SQUAD Constraints
    prob += pulp.lpSum([players.loc[i, 'Price'] * squad_vars[i] for i in players.index]) <= 100.0, "Total_Cost_Constraint"
    prob += pulp.lpSum([squad_vars[i] for i in players.index]) == 15, "Total_Squad_Size_Constraint"
    for pos, count in {'GKP': 2, 'DEF': 5, 'MID': 5, 'FWD': 3}.items():
        prob += pulp.lpSum([squad_vars[i] for i in players.index if players.loc[i, 'Position'] == pos]) == count, f"Squad_{pos}_Constraint"
    for team in players['Team'].unique():
        prob += pulp.lpSum([squad_vars[i] for i in players.index if players.loc[i, 'Team'] == team]) <= 3, f"Team_{team.replace(' ', '_')}_Constraint"
    
    # STARTER Constraints
    prob += pulp.lpSum([starter_vars[i] for i in players.index]) == 11, "Total_Starter_Size_Constraint"
    prob += pulp.lpSum([starter_vars[i] for i in players.index if players.loc[i, 'Position'] == 'GKP']) == 1, "Starter_GKP_Constraint"
    prob += pulp.lpSum([starter_vars[i] for i in players.index if players.loc[i, 'Position'] == 'DEF']) >= 3, "Starter_DEF_Constraint"
    prob += pulp.lpSum([starter_vars[i] for i in players.index if players.loc[i, 'Position'] == 'FWD']) >= 1, "Starter_FWD_Constraint"
    
    # Logical Bridge
    for i in players.index:
        prob += starter_vars[i] <= squad_vars[i], f"Logical_Bridge_{i}"
    print("[+] All constraints are locked in.")

    # 6. Unleash the Thrifty God
    print("\n--- Solving the economic universe... Imposing fiscal discipline... ---")
    prob.solve()
    status = pulp.LpStatus[prob.status]
    print(f"--- THRIFTY SOLUTION FOUND! Status: {status} ---")

    # 7. Reveal the Thrifty Chimera
    if status == 'Optimal':
        squad_indices = [i for i in players.index if squad_vars[i].varValue == 1]
        starter_indices = [i for i in players.index if starter_vars[i].varValue == 1]
        
        full_squad = players.loc[squad_indices]
        starters = players.loc[starter_indices]
        bench = full_squad.drop(starter_indices)

        print("\n*** THE THRIFTY GOD CHIMERA (V3) ***\n")
        print("--- STARTING XI (Points Maximized) ---")
        print(starters[['Surname', 'Team', 'Position', 'Price', 'TP']].sort_values(by=['Position', 'TP'], ascending=[True, False]).to_string())
        
        print("\n--- BENCH (RUTHLESSLY Cost-Optimized) ---")
        print(bench[['Surname', 'Team', 'Position', 'Price', 'TP']].sort_values(by=['Position', 'Price']).to_string())
        
        print("\n-------------------------------------------")
        print(f"Total Squad Cost:       £{full_squad['Price'].sum():.1f}m")
        print(f"Predicted Starting TP:    {starters['TP'].sum()}")
        print(f"Bench Cost:             £{bench['Price'].sum():.1f}m")
        print("-------------------------------------------")
    else:
        print("\n!!! FAILURE: An optimal THRIFTY solution could not be found.")

if __name__ == "__main__":
    forge_thrifty_squad(ENRICHED_DB_PATH)
