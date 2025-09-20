import pandas as pd
import os
import re
import sys

if len(sys.argv) != 2:
    print(">>> ERROR: A gameweek directory must be provided.")
    print(">>> USAGE: python chimera_final_form_v5_rosetta.py gw4")
    sys.exit(1)

# --- Configuration (Mirrors the main script for a perfect simulation) ---
GAMEWEEK_DIR = sys.argv[1]
OMNISCIENT_DB_PATH = f'{GAMEWEEK_DIR}/fpl_master_database_OMNISCIENT.csv'
SET_PIECE_DB_PATH = 'set_pieces.csv'
TEAM_SHORT_TO_FULL = {
    'Spurs': 'Tottenham Hotspur', 'Man City': 'Manchester City', 'Man Utd': 'Manchester United',
    'Newcastle': 'Newcastle United', 'Nott\'m Forest': 'Nottingham Forest', 'West Ham': 'West Ham United',
    'Wolves': 'Wolverhampton Wanderers', 'Leeds': 'Leeds United', 'Brighton': 'Brighton and Hove Albion',
    'Arsenal': 'Arsenal', 'Chelsea': 'Chelsea', 'Bournemouth': 'Bournemouth', 'Everton': 'Everton',
    'Liverpool': 'Liverpool', 'Burnley': 'Burnley', 'Sunderland': 'Sunderland', 'Fulham': 'Fulham',
    'Crystal Palace': 'Crystal Palace', 'Brentford': 'Brentford', 'Aston Villa': 'Aston Villa'
}

def sanitize_name(name: str) -> str:
    """The heart of the Sanitization Bridge (v2 - Hardened)."""
    return re.sub(r'[\.\-\s\(\)]', '', name.lower())

def audit_player_name_resolution():
    """
    Performs a full audit of the player name matching logic between the
    set-piece database and our core player database.
    """
    print("--- PLAYER NAME RESOLUTION AUDIT PROTOCOL ONLINE ---")
    
    # --- Load Data ---
    if not all(os.path.exists(p) for p in [OMNISCIENT_DB_PATH, SET_PIECE_DB_PATH]):
        print("!!! CRITICAL FAILURE: One or more source databases not found. Aborting.")
        return

    players_df = pd.read_csv(OMNISCIENT_DB_PATH)
    set_pieces_df = pd.read_csv(SET_PIECE_DB_PATH)
    print(f"[+] Loaded {len(players_df)} players and {len(set_pieces_df)} teams' set-piece data.")

    # --- Prepare for Join (Replicating the main script's logic) ---
    players_df['match_key'] = players_df['Surname'].apply(sanitize_name)
    players_df['Team_Full_For_Join'] = players_df['Team'].map(TEAM_SHORT_TO_FULL)

    # --- Initialize Audit Counters ---
    success_count = 0
    collision_count = 0
    no_match_count = 0

    print("\n--- BEGINNING ENTITY RESOLUTION AUDIT ---")
    
    # --- Iterate and Audit Every Single Name ---
    for _, row in set_pieces_df.iterrows():
        club_full_name = row['Club']
        duties = {
            'Penalties': str(row['Penalties']).split(','),
            'Direct FKs': str(row['Direct Free Kicks']).split(','),
            'Indirect FKs': str(row['Corners & Indirect Free Kicks']).split(',')
        }
        
        for duty_type, takers in duties.items():
            for taker_name in takers:
                taker_name = taker_name.strip()
                if not taker_name or taker_name.lower() == 'nan':
                    continue

                sanitized_taker = sanitize_name(taker_name)
                
                # Perform the match
                matches = players_df[
                    (players_df['Team_Full_For_Join'] == club_full_name) &
                    (players_df['match_key'].str.contains(sanitized_taker, na=False))
                ]
                
                # Report the findings
                if len(matches) == 1:
                    matched_surname = matches.iloc[0]['Surname']
                    print(f"[  OK  ] '{taker_name}' ({club_full_name}) -> '{matched_surname}'")
                    success_count += 1
                elif len(matches) > 1:
                    colliding_surnames = list(matches['Surname'])
                    print(f"[COLLISION] '{taker_name}' ({club_full_name}) ambiguously matched: {colliding_surnames}")
                    collision_count += 1
                else:
                    print(f"[NO MATCH ] '{taker_name}' ({club_full_name}) - No corresponding player found.")
                    no_match_count += 1

    # --- Final Report ---
    print("\n--- AUDIT SUMMARY ---")
    print(f"  Successful Matches: {success_count}")
    print(f"  Collisions (Critical): {collision_count}")
    print(f"  No Match Found (Warning): {no_match_count}")
    print("-------------------")
    if collision_count == 0 and no_match_count == 0:
        print(">>> VERDICT: The data bridge is structurally sound. Proceed with confidence.")
    else:
        print(">>> VERDICT: Anomalies detected. Review the report and refine data/logic before proceeding.")


if __name__ == "__main__":
    audit_player_name_resolution()
