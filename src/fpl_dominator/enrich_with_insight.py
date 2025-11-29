import os
import sys
import re
import pandas as pd
import yaml


def enrich_with_insight(gameweek_dir: str):
    """
    Loads the enriched database and injects our strategic insights, creating
    the final, prophetic dataset for the Chimera Prophet to consume.
    """
    print("--- [2/4] PROPHETIC ENRICHMENT PROTOCOL ONLINE ---")

    # --- Load Master Configuration ---
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        insight_config = config.get("enrich_insight", {})
        CAPTAINCY_TIERS = insight_config.get("captaincy_tiers", {})
        FORM_LOOKBACK = insight_config.get("form_lookback_weeks", 6)
        print("[+] Master configuration loaded.")
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"!!! WARNING: Could not load or parse config.yaml: {e}. Using default fallbacks.")
        # Define hardcoded fallbacks in case config is missing/broken
        CAPTAINCY_TIERS = {
            "Gods": {"players": ["Haaland", "M.Salah"], "coefficient": 1.5},
            "Demigods": {
                "players": ["João Pedro", "Ekitiké", "Enzo", "Calafiori", "Chalobah"],
                "coefficient": 1.2,
            },
        }
        FORM_LOOKBACK = 6

    # --- Configuration ---
    SOURCE_DB_PATH = f"{gameweek_dir}/fpl_master_database_enriched.csv"
    PROPHETIC_DB_PATH = f"{gameweek_dir}/fpl_master_database_prophetic.csv"

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
                0
            )

        past_gw = current_gw - FORM_LOOKBACK

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
                ]
        else:
            print(
                "    - INFO: Not enough historical data to calculate form. Assigning default form."
            )
            players["Form_Factor"] = players[
                "TP"
            ]

    except Exception as e:
        print(
            f"    - WARNING: Could not calculate form factor. Error: {e}. Assigning default value 0."
        )
        players["Form_Factor"] = 0

    # 1. Create the 'Captaincy_Coef' column, defaulting all players to "Mortal"
    players["Captaincy_Coef"] = 1.0
    print("[+] All players initialized as Mortals (Coef 1.0).")

    # 2. Anoint the Gods and Demigods
    if CAPTAINCY_TIERS:
        for tier_name, tier_data in CAPTAINCY_TIERS.items():
            player_list = tier_data.get("players", [])
            coef = tier_data.get("coefficient", 1.0)

            # Find the indices of players in this tier
            tier_indices = players[players["Surname"].isin(player_list)].index

            # Apply the coefficient
            players.loc[tier_indices, "Captaincy_Coef"] = coef
            print(
                f"    - Anointing {len(tier_indices)} players as {tier_name} (Coef {coef})."
            )
    else:
        print("    - WARNING: No Captaincy Tiers defined in config. Skipping anointment.")


    # 3. Forge the Prophetic Points (PP)
    players["PP"] = (players["TP"] * players["Captaincy_Coef"]).round(2)
    print("[+] 'Prophetic_Points' (PP) metric forged. True value is now visible.")

    # 4. Verification: Show the results for our anointed heroes
    print("\n--- VERIFICATION: THE CHOSEN ONES ---")
    if CAPTAINCY_TIERS:
        anointed_surnames = [
            p for t in CAPTAINCY_TIERS.values() for p in t.get("players", [])
        ]
        verification_df = players[players["Surname"].isin(anointed_surnames)]
        if not verification_df.empty:
            print(
                verification_df[
                    ["Surname", "Team", "TP", "Form_Factor", "Captaincy_Coef", "PP"]
                ].to_string(index=False)
            )
        else:
            print("No anointed players found to verify.")
    else:
        print("No Captaincy Tiers to verify.")


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
