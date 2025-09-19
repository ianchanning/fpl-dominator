import pandas as pd
import os

# --- Configuration ---
DIR = 'gw4'
PROPHETIC_DB_PATH = f'{DIR}/fpl_master_database_prophetic.csv'
FIXTURE_DB_PATH = f'{DIR}/fixtures.csv'
OMNISCIENT_DB_PATH = f'{DIR}/fpl_master_database_OMNISCIENT.csv'

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

# --- The Heart of the Oracle ---

def perform_grand_synthesis(player_path: str, fixture_path: str, output_path: str):
    """
    Merges the Prophetic player database with the Temporal fixture database,
    creating the ultimate Omniscient dataset for our final Chimera.
    """
    print("--- GRAND SYNTHESIS PROTOCOL ONLINE ---")
    
    # 1. Load the Sacred Artifacts
    if not all(os.path.exists(p) for p in [player_path, fixture_path]):
        print("!!! CRITICAL FAILURE: One or more source databases not found. Aborting.")
        return

    players_df = pd.read_csv(player_path)
    fixtures_df = pd.read_csv(fixture_path)
    print("[+] Both Prophetic and Fixture databases have been loaded.")

    # 2. Prepare the Player Data for Merging
    players_df['Team_TLA'] = players_df['Team'].map(TEAM_NAME_TO_TLA)
    if players_df['Team_TLA'].isnull().any():
        print("!!! WARNING: Some team names could not be mapped to an acronym. Check Rosetta Stone.")
    print("[+] Player data prepared with team acronyms for temporal merging.")

    # 3. Calculate the FDR Horizon
    # We group the fixtures by team and calculate the average FDR for the next 5 GWs.
    fdr_horizon = fixtures_df.groupby('Team')['FDR'].mean().reset_index()
    fdr_horizon.rename(columns={'Team': 'Team_TLA', 'FDR': 'FDR_Horizon_5GW'}, inplace=True)
    print("[+] 'FDR_Horizon_5GW' calculated for every team.")

    # 4. The Grand Synthesis (The Merge)
    omniscient_df = pd.merge(players_df, fdr_horizon, on='Team_TLA', how='left')
    print("[+] Prophetic and Temporal realities have been merged.")

    # 5. Forge the Ultimate Metric: Projected Score
    # We divide a player's intrinsic power (PP) by their upcoming difficulty.
    # A lower FDR is better, so this rewards players with easy fixtures.
    omniscient_df['Projected_Score'] = (omniscient_df['PP'] / omniscient_df['FDR_Horizon_5GW']).round(2)
    print("[+] Ultimate metric 'Projected_Score' has been forged.")

    # 6. Verification: Display the most promising assets for the upcoming period
    print("\n--- TOP 15 PROSPECTS (BY PROJECTED SCORE OVER NEXT 5GW) ---")
    print(omniscient_df.sort_values(by='Projected_Score', ascending=False).head(15)
          [['Surname', 'Team', 'PP', 'FDR_Horizon_5GW', 'Projected_Score']].to_string(index=False))

    # 7. Save the Omniscient Database
    try:
        omniscient_df.to_csv(output_path, index=False)
        print(f"\n--- SUCCESS: The OMNISCIENT Database has been forged at '{output_path}' ---")
    except Exception as e:
        print(f"!!! CRITICAL FAILURE: Could not save the omniscient database. Error: {e}")

# --- Main Execution Block ---
if __name__ == "__main__":
    perform_grand_synthesis(PROPHETIC_DB_PATH, FIXTURE_DB_PATH, OMNISCIENT_DB_PATH)
