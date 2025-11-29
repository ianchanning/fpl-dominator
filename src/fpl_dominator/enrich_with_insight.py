import os
import sys
import re
import pandas as pd


# --- The Heart of the Prophet ---
def enrich_with_insight(gameweek_dir: str):
    """
    Loads the enriched database and injects our strategic insights, creating
    the final, prophetic dataset for the Chimera Prophet to consume.
    """
    print("--- [2/4] PROPHETIC ENRICHMENT PROTOCOL ONLINE ---")

    # --- Configuration ---
    SOURCE_DB_PATH = f"{gameweek_dir}/fpl_master_database_enriched.csv"
    PROPHETIC_DB_PATH = f"{gameweek_dir}/fpl_master_database_prophetic.csv"

    # --- The Pirate's Insight (π) ---
    # Here we codify our strategic assessment of player ceilings.
    # This is where we inject our soul into the machine.
    CAPTAINCY_TIERS = {
        # Tier 1: The Gods of Chaos. Their true value is far beyond their base points.
        "Gods": {"players": ["Haaland", "M.Salah"], "coefficient": 1.5},
        # Tier 2: The Demigods. Reliable, high-ceiling assets who are strong captaincy shouts.
        "Demigods": {
            "players": ["João Pedro", "Ekitiké", "Enzo", "Calafiori", "Chalobah"],
            "coefficient": 1.2,
        },
        # Tier 3 (Mortals) is everyone else, with a default coefficient of 1.0.
    }
    if not os.path.exists(SOURCE_DB_PATH):
        print(
            f"!!! CRITICAL FAILURE: Enriched database not found at '{SOURCE_DB_PATH}'. Aborting."
        )
        return False

    try:
        players = pd.read_csv(SOURCE_DB_PATH)
        print(
            f"[+] Intelligence loaded. Preparing to imbue {len(players)} players with strategic insight."
        )
    except Exception as e:
        print(f"!!! CRITICAL FAILURE: Could not read the database. Error: {e}")
        return False

    # === FORM FACTOR CALCULATION (Phase 6) ===
    print("[+] Calculating Form Factor...")
    try:
        current_gw_match = re.search(r"\d+", gameweek_dir)
        if current_gw_match:
            current_gw = int(current_gw_match.group())
        else:
            print(
                f"    - WARNING: Could not extract gameweek number from '{gameweek_dir}'. Defaulting to early gameweek logic."
            )
            current_gw = (
                0  # Default to 0 to trigger the "not enough historical data" path
            )

        past_gw = current_gw - 6

        if past_gw > 0:
            past_db_path = f"gw{past_gw}/fpl_master_database_enriched.csv"
            if os.path.exists(past_db_path):
                df_past = pd.read_csv(past_db_path)

                players = pd.merge(
                    players,
                    df_past[["Surname", "Team", "TP"]],
                    on=["Surname", "Team"],
                    how="left",
                    suffixes=("", "_past"),
                )

                players["TP_past"] = players["TP_past"].fillna(0)
                players["Form_Factor"] = players["TP"] - players["TP_past"]
                players.drop(columns=["TP_past"], inplace=True)
                print(
                    f"    - Form Factor calculated based on performance since GW{past_gw}."
                )

            else:
                print(
                    f"    - WARNING: Past gameweek data not found at '{past_db_path}'. Assigning default form."
                )
                players["Form_Factor"] = players[
                    "TP"
                ]  # Default to total points if no past data
        else:
            print(
                "    - INFO: Not enough historical data to calculate form. Assigning default form."
            )
            players["Form_Factor"] = players[
                "TP"
            ]  # Default to total points for early gameweeks

    except Exception as e:
        print(
            f"    - WARNING: Could not calculate form factor. Error: {e}. Assigning default value 0."
        )
        players["Form_Factor"] = 0

    # 1. Create the 'Captaincy_Coef' column, defaulting all players to "Mortal"
    players["Captaincy_Coef"] = 1.0
    print("[+] All players initialized as Mortals (Coef 1.0).")

    # 2. Anoint the Gods and Demigods
    for tier_name, tier_data in CAPTAINCY_TIERS.items():
        player_list = tier_data["players"]
        coef = tier_data["coefficient"]

        # Find the indices of players in this tier
        tier_indices = players[players["Surname"].isin(player_list)].index

        # Apply the coefficient
        players.loc[tier_indices, "Captaincy_Coef"] = coef
        print(
            f"    - Anointing {len(tier_indices)} players as {tier_name} (Coef {coef})."
        )

    # 3. Forge the Prophetic Points (PP)
    players["PP"] = (players["TP"] * players["Captaincy_Coef"]).round(2)
    print("[+] 'Prophetic_Points' (PP) metric forged. True value is now visible.")

    # 4. Verification: Show the results for our anointed heroes
    print("\n--- VERIFICATION: THE CHOSEN ONES ---")
    anointed_surnames = (
        CAPTAINCY_TIERS["Gods"]["players"] + CAPTAINCY_TIERS["Demigods"]["players"]
    )
    # Also show form factor for verification
    print(
        players[players["Surname"].isin(anointed_surnames)][
            ["Surname", "Team", "TP", "Form_Factor", "Captaincy_Coef", "PP"]
        ].to_string(index=False)
    )

    # 5. Save the Prophetic Database
    try:
        players.to_csv(PROPHETIC_DB_PATH, index=False)
        print(
            f"\n--- SUCCESS: The Prophetic Database has been forged at '{PROPHETIC_DB_PATH}' ---"
        )
        return True
    except Exception as e:
        print(
            f"!!! CRITICAL FAILURE: Could not save the prophetic database. Error: {e}"
        )
        return False


# --- Main Execution Block ---

# This block now only runs if you execute "python enrich_with_insight.py gw5" directly.
# It allows the script to still be used as a standalone tool.
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(">>> ERROR: A gameweek directory must be provided.")
        print(">>> USAGE: python enrich_with_insight.py gw4")
        sys.exit(1)

    gameweek_directory = sys.argv[1]
    enrich_with_insight(gameweek_directory)
