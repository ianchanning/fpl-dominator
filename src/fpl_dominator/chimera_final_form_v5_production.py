import pandas as pd
import pulp
import os
import re
import sys

# --- The Rosetta Stone (π): The key to inter-dimensional communication ---
# Forged directly from the findings of your Reality Audit.
TEAM_SHORT_TO_FULL = {
    'Spurs': 'Tottenham Hotspur', 'Man City': 'Manchester City',
    'Man Utd': 'Manchester United', 'Newcastle': 'Newcastle United',
    'Nott\'m Forest': 'Nottingham Forest', 'West Ham': 'West Ham United',
    'Wolves': 'Wolverhampton Wanderers', 'Leeds': 'Leeds United',
    'Brighton': 'Brighton and Hove Albion',
    # Adding the ones that already match for a complete, robust mapping
    'Arsenal': 'Arsenal', 'Chelsea': 'Chelsea', 'Bournemouth': 'Bournemouth',
    'Everton': 'Everton', 'Liverpool': 'Liverpool', 'Burnley': 'Burnley',
    'Sunderland': 'Sunderland', 'Fulham': 'Fulham', 'Crystal Palace': 'Crystal Palace',
    'Brentford': 'Brentford', 'Aston Villa': 'Aston Villa'
}

def sanitize_name(name: str) -> str:
    """The heart of the Sanitization Bridge (v2 - Hardened)."""
    return re.sub(r'[\.\-\s\(\)]', '', name.lower())

def enrich_with_set_pieces(players_df, set_piece_path, score_model):
    print("[+] Beginning Set-Piece Potency (SPP) enrichment (v5 - Rosetta Protocol)...")
    if not os.path.exists(set_piece_path):
        print(f"!!! CRITICAL FAILURE: Set-piece database not found at '{set_piece_path}'. Aborting enrichment.")
        return players_df

    set_pieces_df = pd.read_csv(set_piece_path)
    players_df['SPP'] = 0.0
    players_df['match_key'] = players_df['Surname'].apply(sanitize_name)
    
    # THE CRITICAL STEP: Use the Rosetta Stone to create a new column for a perfect join.
    players_df['Team_Full_For_Join'] = players_df['Team'].map(TEAM_SHORT_TO_FULL)

    for _, row in set_pieces_df.iterrows():
        club_full_name = row['Club']
        duties = {
            'Penalties': str(row['Penalties']).split(','),
            'Direct Free Kicks': str(row['Direct Free Kicks']).split(','),
            'Corners & Indirect Free Kicks': str(row['Corners & Indirect Free Kicks']).split(',')
        }
        
        for duty_type, takers in duties.items():
            for i, taker_name in enumerate(takers):
                sanitized_taker = sanitize_name(taker_name.strip())
                
                # THE FIX: We now match on the new, perfect, translated full name column.
                target_indices = players_df[
                    (players_df['Team_Full_For_Join'] == club_full_name) &
                    (players_df['match_key'].str.contains(sanitized_taker, na=False))
                ].index
                
                if not target_indices.empty:
                    score = score_model[duty_type]['primary'] if i == 0 else score_model[duty_type]['secondary']
                    players_df.loc[target_indices, 'SPP'] += score

    # Clean up our temporary join columns
    players_df.drop(columns=['match_key', 'Team_Full_For_Join'], inplace=True)
    print("[+] SPP enrichment complete. Realities have been aligned.")
    return players_df

def forge_final_form_squad(gameweek_dir: str):
    print("--- [4/4] CHIMERA FINAL FORM ENGINE (V5 - PRODUCTION) ONLINE ---")

    # --- Configuration ---
    OMNISCIENT_DB_PATH = f'{gameweek_dir}/fpl_master_database_OMNISCIENT.csv'
    SET_PIECE_DB_PATH = 'set_pieces.csv'
    FINAL_FORM_DB_PATH = f'{gameweek_dir}/fpl_master_database_FINAL_v5.csv'
    THRIFT_FACTOR = 0.001
    SPP_SCORES = {
        'Penalties': {'primary': 5.0, 'secondary': 2.5},
        'Direct Free Kicks': {'primary': 2.5, 'secondary': 1.25},
        'Corners & Indirect Free Kicks': {'primary': 1.5, 'secondary': 0.75}
    }

    if not os.path.exists(OMNISCIENT_DB_PATH):
        print(f"!!! CRITICAL FAILURE: Omniscient Database not found at '{OMNISCIENT_DB_PATH}'. Aborting.")
        return False

    players = pd.read_csv(OMNISCIENT_DB_PATH)
    players = enrich_with_set_pieces(players, SET_PIECE_DB_PATH, SPP_SCORES)
    
    players['Final_Score'] = ((players['PP'] + players['SPP']) / players['FDR_Horizon_5GW']).round(2)
    players.to_csv(FINAL_FORM_DB_PATH, index=False)
    print(f"[+] Final Form database (v5) forged at '{FINAL_FORM_DB_PATH}'.")

    print("\n>>> LAUNCHING FINAL FORM SIMULATION (V5)...")
    prob = pulp.LpProblem("FPL_Final_Form_v5", pulp.LpMaximize)
    
    # ... (The entire PuLP section is identical to v4, as the logic is now perfect) ...
    squad_vars = pulp.LpVariable.dicts("in_squad", players.index, cat='Binary')
    starter_vars = pulp.LpVariable.dicts("is_starter", players.index, cat='Binary')

    starter_final_score = pulp.lpSum([players.loc[i, 'Final_Score'] * starter_vars[i] for i in players.index])
    bench_cost_penalty = pulp.lpSum([(squad_vars[i] - starter_vars[i]) * players.loc[i, 'Price'] * THRIFT_FACTOR for i in players.index])
    prob += starter_final_score - bench_cost_penalty, "Final_Form_Objective_v5"

    prob += pulp.lpSum([players.loc[i, 'Price'] * squad_vars[i] for i in players.index]) <= 100.0, "Cost"
    prob += pulp.lpSum([squad_vars[i] for i in players.index]) == 15, "SquadSize"
    for pos, count in {'GKP': 2, 'DEF': 5, 'MID': 5, 'FWD': 3}.items():
        prob += pulp.lpSum([squad_vars[i] for i in players.index if players.loc[i, 'Position'] == pos]) == count, f"Squad_{pos}"
    for team in players['Team_TLA'].unique():
        prob += pulp.lpSum([squad_vars[i] for i in players.index if players.loc[i, 'Team_TLA'] == team]) <= 3, f"Team_{team.replace(' ', '_')}"
    prob += pulp.lpSum([starter_vars[i] for i in players.index]) == 11, "StarterSize"
    prob += pulp.lpSum([starter_vars[i] for i in players.index if players.loc[i, 'Position'] == 'GKP']) == 1, "Starter_GKP"
    prob += pulp.lpSum([starter_vars[i] for i in players.index if players.loc[i, 'Position'] == 'DEF']) >= 3, "Starter_DEF"
    prob += pulp.lpSum([starter_vars[i] for i in players.index if players.loc[i, 'Position'] == 'FWD']) >= 1, "Starter_FWD"
    for i in players.index: prob += starter_vars[i] <= squad_vars[i], f"Bridge_{i}"

    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    status = pulp.LpStatus[prob.status]

    if status == 'Optimal':
        squad_indices = [i for i in players.index if squad_vars[i].varValue == 1]
        starter_indices = [i for i in players.index if starter_vars[i].varValue == 1]
        squad = players.loc[squad_indices]
        starters = players.loc[starter_indices]
        bench = squad.drop(starter_indices)

        # --- Enforce Positional Order for Printing ---
        position_order = ['GKP', 'DEF', 'MID', 'FWD']
        starters['Position'] = pd.Categorical(starters['Position'], categories=position_order, ordered=True)
        bench['Position'] = pd.Categorical(bench['Position'], categories=position_order, ordered=True)
        
        print("\n" + "="*20 + " FINAL FORM SQUAD (V5) FORGED " + "="*20)
        print("\n--- STARTING XI (Final Score Maximized) ---")
        print(starters[['Surname', 'Team', 'Position', 'Price', 'Final_Score']].sort_values(by=['Position', 'Final_Score'], ascending=[True, False]).to_string(index=False))
        print("\n--- BENCH (RUTHLESSLY Cost-Optimized) ---")
        print(bench[['Surname', 'Team', 'Position', 'Price', 'Final_Score']].sort_values(by=['Position', 'Price']).to_string(index=False))
        print("\n-------------------------------------------")
        print(f"Total Squad Cost:          £{squad['Price'].sum():.1f}m")
        print(f"Projected Starting Score:    {starters['Final_Score'].sum():.2f}")
        print(f"Money in the Bank:         £{100.0 - squad['Price'].sum():.1f}m")
        print("-------------------------------------------")
        return True
    else:
        print(f"\n!!! FAILURE: An optimal FINAL FORM solution could not be found. Status: {status}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(">>> ERROR: A gameweek directory must be provided.")
        print(">>> USAGE: python chimera_final_form_v5_production.py gw4")
        sys.exit(1)

    gameweek_directory = sys.argv[1]
    forge_final_form_squad(gameweek_directory)
