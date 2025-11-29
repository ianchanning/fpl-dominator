import os

import pandas as pd


def audit_team_name_realities(gameweek_dir: str):
    """
    Compares the team name conventions in two separate databases and
    reports any and all discrepancies. A pure diagnostic tool.
    """
    PLAYER_DB_PATH = f"{gameweek_dir}/fpl_master_database_OMNISCIENT.csv"
    SET_PIECE_DB_PATH = "set_pieces.csv"

    print("--- REALITY AUDIT PROTOCOL ONLINE ---")

    if not all(os.path.exists(p) for p in [PLAYER_DB_PATH, SET_PIECE_DB_PATH]):
        print("!!! CRITICAL FAILURE: One or more source databases not found. Aborting.")
        if not os.path.exists(PLAYER_DB_PATH):
            print(f"!!! NOTE: Player database not found at '{PLAYER_DB_PATH}'.")
            print(f"!!! Have you run the main gauntlet for '{gameweek_dir}' yet?")
        return

    # Load the unique team names from each universe
    player_teams = set(pd.read_csv(PLAYER_DB_PATH)["Team"].unique())
    set_piece_teams = set(pd.read_csv(SET_PIECE_DB_PATH)["Club"].unique())

    print(f"[+] Found {len(player_teams)} unique teams in the Player Database.")
    print(f"[+] Found {len(set_piece_teams)} unique teams in the Set-Piece Database.")

    # Use the beautiful power of set theory to find the differences
    player_db_only = player_teams.difference(set_piece_teams)
    set_piece_db_only = set_piece_teams.difference(player_teams)

    print("\n--- AIRLOCK ANOMALY REPORT ---")
    if not player_db_only and not set_piece_db_only:
        print(
            ">>> SUCCESS: All team names are perfectly aligned across realities. No anomalies detected."
        )
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


# This script is now intended to be used as a library.
# To run it directly, you would need to add a __main__ block like this:
# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) != 2:
#         print(">>> ERROR: A gameweek directory must be provided.")
#         print(">>> USAGE: python audit_realities.py gw11")
#     else:
#         audit_team_name_realities(sys.argv[1])
