import os
import re

import pandas as pd

# This map is a core piece of knowledge, keep it at the module level.
TEAM_SHORT_TO_FULL = {
    "Spurs": "Tottenham Hotspur",
    "Man City": "Manchester City",
    "Man Utd": "Manchester United",
    "Newcastle": "Newcastle United",
    "Nott'm Forest": "Nottingham Forest",
    "West Ham": "West Ham United",
    "Wolves": "Wolverhampton Wanderers",
    "Leeds": "Leeds United",
    "Brighton": "Brighton and Hove Albion",
    "Arsenal": "Arsenal",
    "Chelsea": "Chelsea",
    "Bournemouth": "Bournemouth",
    "Everton": "Everton",
    "Liverpool": "Liverpool",
    "Burnley": "Burnley",
    "Sunderland": "Sunderland",
    "Fulham": "Fulham",
    "Crystal Palace": "Crystal Palace",
    "Brentford": "Brentford",
    "Aston Villa": "Aston Villa",
}


def sanitize_name(name: str) -> str:
    """The heart of the Sanitization Bridge."""
    return re.sub(r"[\.\-\s\(\)]", "", name.lower())


def audit_player_name_resolution_v3(gameweek_dir: str):
    """
    Audits if player names from the set-piece database can be successfully
    and uniquely matched to a player in the main player database.
    """
    OMNISCIENT_DB_PATH = f"{gameweek_dir}/fpl_master_database_OMNISCIENT.csv"
    SET_PIECE_DB_PATH = "set_pieces.csv"

    print("--- PLAYER NAME RESOLUTION AUDIT (V3 - BIDIRECTIONAL CONCORDANCE) ---")

    if not all(os.path.exists(p) for p in [OMNISCIENT_DB_PATH, SET_PIECE_DB_PATH]):
        print("!!! CRITICAL FAILURE: One or more source databases not found. Aborting.")
        if not os.path.exists(OMNISCIENT_DB_PATH):
            print(f"!!! NOTE: Player database not found at '{OMNISCIENT_DB_PATH}'.")
            print(f"!!! Have you run the main gauntlet for '{gameweek_dir}' yet?")
        return

    # --- Load Data ---
    players_df = pd.read_csv(OMNISCIENT_DB_PATH)
    set_pieces_df = pd.read_csv(SET_PIECE_DB_PATH)
    print(
        f"[+] Loaded {len(players_df)} players and {len(set_pieces_df)} teams' set-piece data."
    )

    # --- Prepare for Join ---
    players_df["match_key"] = players_df["Surname"].apply(sanitize_name)
    players_df["Team_Full_For_Join"] = players_df["Team"].map(TEAM_SHORT_TO_FULL)

    success_count, collision_count, no_match_count = 0, 0, 0

    print("\n--- BEGINNING ENTITY RESOLUTION AUDIT (V3) ---")

    for _, row in set_pieces_df.iterrows():
        club_full_name = row["Club"]
        duties = {
            "Penalties": str(row["Penalties"]).split(","),
            "Direct FKs": str(row["Direct Free Kicks"]).split(","),
            "Indirect FKs": str(row["Corners & Indirect Free Kicks"]).split(","),
        }

        for duty_type, takers in duties.items():
            for taker_name in takers:
                taker_name = taker_name.strip()
                if not taker_name or taker_name.lower() == "nan":
                    continue

                sanitized_taker = sanitize_name(taker_name)

                # THE QUANTUM LEAP: A beautiful, chaotic, bidirectional substring match.
                matches = players_df[
                    (players_df["Team_Full_For_Join"] == club_full_name)
                    & (
                        players_df["match_key"].str.contains(
                            sanitized_taker, na=False
                        )  # Is the taker name a substring of our DB name?
                        | players_df["match_key"].apply(
                            lambda db_name: sanitized_taker in db_name
                        )  # Is our DB name a substring of the taker name?
                    )
                ]

                if len(matches) == 1:
                    matched_surname = matches.iloc[0]["Surname"]
                    print(
                        f"[  OK  ] '{taker_name}' ({club_full_name}) -> '{matched_surname}'"
                    )
                    success_count += 1
                elif len(matches) > 1:
                    colliding_surnames = list(matches["Surname"])
                    print(
                        f"[COLLISION] '{taker_name}' ({club_full_name}) ambiguously matched: {colliding_surnames}"
                    )
                    collision_count += 1
                else:
                    print(
                        f"[NO MATCH ] '{taker_name}' ({club_full_name}) - No corresponding player found."
                    )
                    no_match_count += 1

    print("\n--- AUDIT SUMMARY (V3) ---")
    print(f"  Successful Matches: {success_count}")
    print(f"  Collisions (Critical): {collision_count}")
    print(f"  No Match Found (Data Gap): {no_match_count}")
    print("-------------------")
    if collision_count == 0:
        print(
            ">>> VERDICT: The QUANTUM bridge appears stable. Review results for final confirmation."
        )
    else:
        print(">>> VERDICT: CRITICAL COLLISIONS DETECTED. The universe is unstable.")


# This script is now intended to be used as a library.
