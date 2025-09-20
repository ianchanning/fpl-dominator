import pandas as pd
import os
import sys

if len(sys.argv) != 2:
    print(">>> ERROR: A gameweek directory must be provided.")
    print(">>> USAGE: python chimera_final_form_v5_rosetta.py gw4")
    sys.exit(1)

# --- Configuration ---
GAMEWEEK_DIR = sys.argv[1]
PLAYER_DB_PATH = f'{GAMEWEEK_DIR}/fpl_master_database_OMNISCIENT.csv' # Using this as it has the short names
SET_PIECE_DB_PATH = 'set_pieces.csv'

def audit_team_name_realities(player_path: str, set_piece_path: str):
    """
    Compares the team name conventions in two separate databases and
    reports any and all discrepancies. A pure diagnostic tool.
    """
    print("--- REALITY AUDIT PROTOCOL ONLINE ---")
    
    if not all(os.path.exists(p) for p in [player_path, set_piece_path]):
        print("!!! CRITICAL FAILURE: One or more source databases not found. Aborting.")
        return

    # Load the unique team names from each universe
    player_teams = set(pd.read_csv(player_path)['Team'].unique())
    set_piece_teams = set(pd.read_csv(set_piece_path)['Club'].unique())
    
    print(f"[+] Found {len(player_teams)} unique teams in the Player Database.")
    print(f"[+] Found {len(set_piece_teams)} unique teams in the Set-Piece Database.")
    
    # Use the beautiful power of set theory to find the differences
    player_db_only = player_teams.difference(set_piece_teams)
    set_piece_db_only = set_piece_teams.difference(player_teams)
    
    print("\n--- AIRLOCK ANOMALY REPORT ---")
    if not player_db_only and not set_piece_db_only:
        print(">>> SUCCESS: All team names are perfectly aligned across realities. No anomalies detected.")
    else:
        if player_db_only:
            print("\n[!] Teams found ONLY in the Player Database (short names):")
            for team in sorted(list(player_db_only)):
                print(f"    - {team}")
        
        if set_piece_db_only:
            print("\n[!] Teams found ONLY in the Set-Piece Database (full names):")
            for team in sorted(list(set_piece_db_only)):
                print(f"    - {team}")
    print("\n--- END OF REPORT ---")

if __name__ == "__main__":
    audit_team_name_realities(PLAYER_DB_PATH, SET_PIECE_DB_PATH)
