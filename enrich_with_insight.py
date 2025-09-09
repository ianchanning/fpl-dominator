import pandas as pd
import os

# --- Configuration ---
SOURCE_DB_PATH = 'fpl_master_database_enriched.csv'
PROPHETIC_DB_PATH = 'fpl_master_database_prophetic.csv'

# --- The Pirate's Insight (π) ---
# Here we codify our strategic assessment of player ceilings.
# This is where we inject our soul into the machine.
CAPTAINCY_TIERS = {
    # Tier 1: The Gods of Chaos. Their true value is far beyond their base points.
    "Gods": {
        "players": ['Haaland', 'M.Salah'],
        "coefficient": 1.5
    },
    # Tier 2: The Demigods. Reliable, high-ceiling assets who are strong captaincy shouts.
    "Demigods": {
        "players": ['João Pedro', 'Ekitiké', 'Enzo', 'Calafiori', 'Chalobah'],
        "coefficient": 1.2
    }
    # Tier 3 (Mortals) is everyone else, with a default coefficient of 1.0.
}

# --- The Heart of the Prophet ---

def imbue_with_prophecy(source_path: str, output_path: str):
    """
    Loads the enriched database and injects our strategic insights, creating
    the final, prophetic dataset for the Chimera Prophet to consume.
    """
    print("--- PROPHETIC ENRICHMENT PROTOCOL ONLINE ---")
    if not os.path.exists(source_path):
        print(f"!!! CRITICAL FAILURE: Enriched database not found at '{source_path}'. Aborting.")
        return

    try:
        players = pd.read_csv(source_path)
        print(f"[+] Intelligence loaded. Preparing to imbue {len(players)} players with strategic insight.")
    except Exception as e:
        print(f"!!! CRITICAL FAILURE: Could not read the database. Error: {e}")
        return

    # 1. Create the 'Captaincy_Coef' column, defaulting all players to "Mortal"
    players['Captaincy_Coef'] = 1.0
    print("[+] All players initialized as Mortals (Coef 1.0).")

    # 2. Anoint the Gods and Demigods
    for tier_name, tier_data in CAPTAINCY_TIERS.items():
        player_list = tier_data['players']
        coef = tier_data['coefficient']
        
        # Find the indices of players in this tier
        tier_indices = players[players['Surname'].isin(player_list)].index
        
        # Apply the coefficient
        players.loc[tier_indices, 'Captaincy_Coef'] = coef
        print(f"    - Anointing {len(tier_indices)} players as {tier_name} (Coef {coef}).")

    # 3. Forge the Prophetic Points (PP)
    players['PP'] = (players['TP'] * players['Captaincy_Coef']).round(2)
    print("[+] 'Prophetic_Points' (PP) metric forged. True value is now visible.")

    # 4. Verification: Show the results for our anointed heroes
    print("\n--- VERIFICATION: THE CHOSEN ONES ---")
    anointed_surnames = CAPTAINCY_TIERS['Gods']['players'] + CAPTAINCY_TIERS['Demigods']['players']
    print(players[players['Surname'].isin(anointed_surnames)][['Surname', 'Team', 'TP', 'Captaincy_Coef', 'PP']].to_string(index=False))

    # 5. Save the Prophetic Database
    try:
        players.to_csv(output_path, index=False)
        print(f"\n--- SUCCESS: The Prophetic Database has been forged at '{output_path}' ---")
    except Exception as e:
        print(f"!!! CRITICAL FAILURE: Could not save the prophetic database. Error: {e}")

# --- Main Execution Block ---

if __name__ == "__main__":
    imbue_with_prophecy(SOURCE_DB_PATH, PROPHETIC_DB_PATH)
