import pandas as pd
import os
import sys
import numpy as np


# --- The Heart of the Oracle ---

def perform_grand_synthesis(gameweek_dir: str):
    """
    Merges the Prophetic player database with the Temporal fixture database,
    creating the ultimate Omniscient dataset for our final Chimera.
    """
    print("--- [3/4] GRAND SYNTHESIS PROTOCOL ONLINE ---")

    # --- Configuration ---
    PROPHETIC_DB_PATH = f'{gameweek_dir}/fpl_master_database_prophetic.csv'
    FIXTURE_DB_PATH = f'{gameweek_dir}/fixtures.csv'
    OMNISCIENT_DB_PATH = f'{gameweek_dir}/fpl_master_database_OMNISCIENT.csv'

    # --- The Pirate's Rosetta Stone (π) ---
    # A crucial mapping to bridge the gap between our two data sources.
    TEAM_NAME_TO_TLA = {
        'Arsenal': 'ARS', 'Aston Villa': 'AVL', 'Brighton': 'BHA',
        'Bournemouth': 'BOU', 'Brentford': 'BRE', 'Burnley': 'BUR',
        'Chelsea': 'CHE', 'Crystal Palace': 'CRY', 'Everton': 'EVE',
        'Fulham': 'FUL', 'Leeds': 'LEE', 'Liverpool': 'LIV',
        'Man City': 'MCI', 'Man Utd': 'MUN', 'Newcastle': 'NEW',
        'Nott\'m Forest': 'NFO', 'Sunderland': 'SUN', 'Spurs': 'TOT',
        'West Ham': 'WHU', 'Wolves': 'WOL'
    }
    
    # 1. Load the Sacred Artifacts
    if not all(os.path.exists(p) for p in [PROPHETIC_DB_PATH, FIXTURE_DB_PATH]):
        print("!!! CRITICAL FAILURE: One or more source databases not found. Aborting.")
        return False

    players_df = pd.read_csv(PROPHETIC_DB_PATH)
    fixtures_df = pd.read_csv(FIXTURE_DB_PATH)
    print("[+] Both Prophetic and Fixture databases have been loaded.")

    # 2. Prepare the Player Data for Merging
    players_df['Team_TLA'] = players_df['Team'].map(TEAM_NAME_TO_TLA)
    if players_df['Team_TLA'].isnull().any():
        print("!!! WARNING: Some team names could not be mapped to an acronym. Check Rosetta Stone.")
    print("[+] Player data prepared with team acronyms for temporal merging.")

    # 3. Calculate the FDR Horizon (Trinity Protocol)
    # We group fixtures by team and calculate the mean FDR for Attack and Defence separately.
    fdr_horizon = fixtures_df.groupby('Team').agg(
        FDR_A_Horizon_5GW=('FDR_A', 'mean'),
        FDR_D_Horizon_5GW=('FDR_D', 'mean')
    ).reset_index()
    fdr_horizon.rename(columns={'Team': 'Team_TLA'}, inplace=True)
    print("[+] Trinity FDR Horizons (Attack/Defence) calculated for every team.")

    # 4. The Grand Synthesis (The Merge)
    omniscient_df = pd.merge(players_df, fdr_horizon, on='Team_TLA', how='left')
    print("[+] Prophetic and Temporal realities have been merged.")

    # 5. Positional Bifurcation: Forge the Effective FDR
    # Apply the correct FDR based on player position.
    omniscient_df['Effective_FDR_Horizon_5GW'] = np.where(
        omniscient_df['Position'].isin(['GKP', 'DEF']),
        omniscient_df['FDR_D_Horizon_5GW'],
        omniscient_df['FDR_A_Horizon_5GW']
    )
    print("[+] 'Effective_FDR_Horizon_5GW' forged using positional bifurcation logic.")

    # 6. Forge the Ultimate Metric: Projected Score
    # We divide a player's intrinsic power (PP) by their upcoming effective difficulty.
    omniscient_df['Projected_Score'] = (omniscient_df['PP'] / omniscient_df['Effective_FDR_Horizon_5GW']).round(2)
    print("[+] Ultimate metric 'Projected_Score' has been forged using effective FDR.")

    # 7. Verification: Display the most promising assets for the upcoming period
    print("\n--- TOP 15 PROSPECTS (BY PROJECTED SCORE OVER NEXT 5GW) ---")
    print(omniscient_df.sort_values(by='Projected_Score', ascending=False).head(15)
          [['Surname', 'Team', 'PP', 'Effective_FDR_Horizon_5GW', 'Projected_Score']].to_string(index=False))

    # 8. Save the Omniscient Database
    try:
        omniscient_df.to_csv(OMNISCIENT_DB_PATH, index=False)
        print(f"\n--- SUCCESS: The OMNISCIENT Database has been forged at '{OMNISCIENT_DB_PATH}' ---")
        return True
    except Exception as e:
        print(f"!!! CRITICAL FAILURE: Could not save the omniscient database. Error: {e}")
        return False

# --- Main Execution Block ---
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(">>> ERROR: A gameweek directory must be provided.")
        print(">>> USAGE: python chimera_final_form_v5_rosetta.py gw4")
        sys.exit(1)

    gameweek_directory = sys.argv[1]
    perform_grand_synthesis(gameweek_directory)
